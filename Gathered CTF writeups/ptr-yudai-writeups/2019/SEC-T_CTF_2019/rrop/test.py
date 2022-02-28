from ptrlib import *
import ctypes

glibc = ctypes.cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc-2.27.so')

# 1162 +
# 2009
# 4564
# 7282 +
for i in range(7283, 0x10000):
    glibc.srand(i)
    gadgets = b''
    for j in range(0x2000):
        gadgets += p32(glibc.rand())
    # find 'pop rax', 'pop rdi' and 'syscall'
    try:
        assert (b'\x54\x5f\xc3' in gadgets) # mov rdi, rsp;
        assert (b'\x5f\xc3' in gadgets and b'\x58\xc3' in gadgets) or (b'\x5f\x58\xc3' in gadgets) or (b'\x58\x5f\xc3' in gadgets) # pop rdi; pop rax;
        assert b'\x0f\x05' in gadgets # syscall
    except:
        continue
    # search for rop gadgets
    ofs = 0
    cnt = 0
    while b'\xc3' in gadgets[ofs:]:
        ofs = gadgets.index(b'\xc3', ofs)
        #print(gadgets[ofs - 10:][:11].hex())
        if b'\x48\x89' in gadgets[ofs - 10:][:11]:
            print(gadgets[ofs - 10:][:11].hex())
            cnt += 1
        #if b'\x08' in gadgets[ofs - 12:][:13]:
        #    print(gadgets[ofs - 12:][:13].hex())
        #    cnt += 1
        ofs += 1
    #if cnt == 0: continue
    print("Found: {}".format(i))
    break

with open("gadgets", "wb") as f:
    f.write(gadgets)
