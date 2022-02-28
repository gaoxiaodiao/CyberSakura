import string as STR

def sub_194():
    global memory, string
    pos0 = 0
    pos1 = 0
    for i in range(0x30): # rdx=0x30
        pos0 = (pos0 + 1) & 0xff
        xmm2 = ord(memory[pos0])
        pos1 = (pos1 + xmm2) & 0xff
        xmm3 = ord(memory[pos1])
        memory = memory[:pos0] + chr(xmm3 & 0xff) + memory[pos0+1:]
        memory = memory[:pos1] + chr(xmm2 & 0xff) + memory[pos1+1:]
        string = string[:i] + chr(ord(string[i]) ^ ord(memory[(xmm2 + xmm3) & 0xff])) + string[i+1:]

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
        xmm0 = ord(memory[x])
        r9 = (r9 + ord(memory[x]) + ord(password[r10])) & 0xff
        memory = memory[:x] + chr(ord(memory[r9])) + memory[x+1:]
        memory = memory[:r9] + chr(xmm0) + memory[r9+1:]
        r10 = (r10 + 1) % 8

def p64(s):
    import struct
    return struct.pack("<Q", s)
def u64(s):
    import struct
    return struct.unpack("<Q", s)[0]

table = STR.printable[:-5]
save = [44, 36, 82, 0]
for c1 in range(save[0], len(table)):
    for c2 in range(save[1], len(table)):
        for c3 in range(save[2], len(table)):
            for c4 in range(save[3], len(table)):
                pattern = [c1, c2, c3, c4]
                patternw = table[c1] + table[c2] + table[c3] + table[c4]
                password = patternw + "wT96"

                memory = ''
                string = "\xf6\x2c\x72\x1a\x03\x99\x0e\x78\xbd\x90\xe9\x68\xd0\x69\x37\x29"
                string += "\xf8\x12\xf4\xe5\xd0\xfb\xf3\x7e\x72\x61\x79\x19\xed\x44\x12\x52"
                string += "\xf5\xf9\xaa\x14\x36\x0d\x1f\xb2\x52\x6b\xf2\x6a\xda\x9d\xec\x3c"

                sub_113()
                sub_194()
                ret, text = u64(string[:8]), string[8:]
                d = 0x115c28da834feffd ^ ret
                c = 0x665f336b1a566b19 ^ d
                b = 0x393b415f5a590044 ^ c
                a = 0x3255557376f68 ^ b
                flag = p64(a) + p64(b) + p64(c) + p64(d)[:-4]
                for c in flag:
                    if c not in STR.printable:
                        break
                else:
                    print("=" * 50)
                    print(pattern)
                    print(password)
                    print(text)
                    print(flag)
