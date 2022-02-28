from ptrlib import *

with open("firmware.bin", "rb") as f:
    f.seek(0x20)
    s = f.read(0x40 * 9)

def blackbox(a, b):
    output = b''
    for i in range(len(a)):
        output += bytes([(a[i] & b[i]) % 0x100])
    return output

def trim(s):
    output = ''
    for i in range(1, len(s), 2):
        output += s[i]
    return output

w = ''.join([chr(i) for i in range(0x3d, 0x7f)])
#print(w)
w = s[:0x40]
delta = 0x10
for i in range(0, 9):
    q = blackbox(w, s[i * 0x40:(i + 1) * 0x40])
    #print(q)
    #q = str2bytes(trim(bytes2str(q)))
    p = bin(int.from_bytes(q, byteorder='big'))[2:].zfill(528)
    #print(p)
    #p = trim(p)
    print(p[:200].replace("1","#").replace("0","."))
    #for j in range(0, len(p), delta):
    #    print(p[j:j+delta])
