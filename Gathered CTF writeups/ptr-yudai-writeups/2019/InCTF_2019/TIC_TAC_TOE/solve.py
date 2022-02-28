from ptrlib import *
import string

data2 = []
with open("Tic.exe", "rb") as f:
    f.seek(0xd8a8)
    for i in range(0x20):
        data2.append(u32(f.read(4)))

flag = []
xs = []
#table = "abcdefghijklmnopqrstuvwxyz{_}"
table = string.printable[:-6]

fix = {
    0: ord('i'),
    2: ord('c'),
    4: ord('f'),
    6: ord('w'),
    8: ord('W'),
    10: ord('Y'),
    12: ord('u'),
    14: ord('c'),
    16: ord('4'),
    18: ord('k'),
    22: ord('m'),
    26: ord('3'),
    28: ord('h'),
    30: ord('d'),
}

for i in range(0x10):
    flag.append([])
    for c in range(0x10000):
        c1 = c & 0xff
        c2 = c >> 8
        if i*2 in fix: c1 = fix[i*2]
        if i*2+1 in fix: c2 = fix[i*2+1]
        if chr(c1) not in table: continue
        if chr(c2) not in table: continue
        xs1 = c1 ^ (i*2 + data2[i*2])
        xs2 = c2 ^ (i*2+1 + data2[i*2+1])
        if xs1 % 8 != 0: continue
        if xs2 % 7 != 0: continue
        if xs1 // 8 != xs2 // 7: continue
        #if not (10 <= xs1 // 8 <= 25): continue
        #if not (10 <= xs2 // 7 <= 25): continue
        flag[-1].append(chr(c1) + chr(c2))
        if i*2 in fix: break
        if i*2+1 in fix: break

result = ""
for piece in flag:
    if piece:
        result += piece[0]
    else:
        result += "??"

print(result)
# inctf{w0W_Y0u_cr4ck3d_my_m3th0d}
