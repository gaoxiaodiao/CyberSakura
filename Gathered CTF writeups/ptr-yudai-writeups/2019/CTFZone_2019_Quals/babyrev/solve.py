import re

key = b'?' * (0x50*6)
key = b'\xdb' + key[1:]
with open("disasm.txt", "r") as f:
    for line in f:
        if 'cmpb' not in line: continue
        r = re.findall("\$0x([0-9a-f]+),0x([0-9a-f]+)\(%si\)", line)
        if r:
            val = int(r[0][0], 16)
            ofs = int(r[0][1], 16)
            key = key[:ofs] + bytes([val]) + key[ofs+1:]

for i in range(6):
    for j in range(0x50):
        c = key[i*0x50+j]
        if c == 0xdb: c = ord('#')
        elif c == 0xcd: c = ord('.')
        elif c != 0x20 and c != 0x0a: c = ord('_')
        print(chr(c), end="")
