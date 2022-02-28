from ptrlib import *
import string as STR

def sub_194():
    global memory, string
    pos0 = 0
    pos1 = 0
    for i in range(0x30): # rdx=0x30
        pos0 = (pos0 + 1) & 0xff
        xmm2 = memory[pos0]
        pos1 = (pos1 + xmm2) & 0xff
        xmm3 = memory[pos1]
        memory = memory[:pos0] + bytes([xmm3 & 0xff]) + memory[pos0+1:]
        memory = memory[:pos1] + bytes([xmm2 & 0xff]) + memory[pos1+1:]
        string = string[:i] + bytes([string[i] ^ memory[(xmm2 + xmm3) & 0xff]]) + string[i+1:]

def sub_113():
    global memory, password
    memory = b""
    delta = 0x0808080808080808
    seed = 0x0706050403020100
    for i in range(0x20):
        memory += p64(seed)
        seed = (seed + delta) & 0xffffffffffffffff
    r9 = 0
    r10 = 0
    for x in range(0x100):
        xmm0 = memory[x]
        r9 = (r9 + memory[x] + password[r10]) & 0xff
        memory = memory[:x] + bytes([memory[r9]]) + memory[x+1:]
        memory = memory[:r9] + bytes([xmm0]) + memory[r9+1:]
        r10 = (r10 + 1) % 8

table = STR.ascii_letters + STR.digits
#save = [8,46,13,10]
save = [26, 0, 0, 0]
for c1 in range(save[0], len(table)):
    for c2 in range(save[1], len(table)):
        for c3 in range(save[2], len(table)):
            for c4 in range(save[3], len(table)):
                pattern = [c1, c2, c3, c4]
                patternw = table[c1] + table[c2] + table[c3] + table[c4]
                password = str2bytes(patternw + "wT96")

                memory = b''
                string = b"\xf6\x2c\x72\x1a\x03\x99\x0e\x78\xbd\x90\xe9\x68\xd0\x69\x37\x29"
                string += b"\xf8\x12\xf4\xe5\xd0\xfb\xf3\x7e\x72\x61\x79\x19\xed\x44\x12\x52"
                string += b"\xf5\xf9\xaa\x14\x36\x0d\x1f\xb2\x52\x6b\xf2\x6a\xda\x9d\xec\x3c"

                sub_113()
                sub_194()
                ret, text = u64(string[:8]), string[8:]
                d = 0x115c28da834feffd ^ ret
                c = 0x665f336b1a566b19 ^ d
                b = 0x393b415f5a590044 ^ c
                a = 0x3255557376f68 ^ b
                flag = (p64(a) + p64(b) + p64(c) + p64(d))[:-4]
                for c in flag:
                    if chr(c) not in STR.printable:
                        break
                else:
                    print("=" * 50)
                    print(pattern)
                    print(password)
                    print(text)
                    print(flag)
