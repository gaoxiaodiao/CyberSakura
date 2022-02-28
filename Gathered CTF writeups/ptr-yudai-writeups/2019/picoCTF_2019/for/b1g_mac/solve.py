from ptrlib import *

with open("b1g_mac.zip", "rb") as f:
    buf = f.read()

flag = b''
ofs = u32(buf[-6:-2])
while buf[ofs:ofs+4] == b'PK\x01\x02':
    len_name = u16(buf[ofs+0x1c:ofs+0x1e])
    len_extra = u16(buf[ofs+0x1e:ofs+0x20])
    filename = buf[ofs+0x2e:ofs+0x2e+len_name]
    extra = buf[ofs+0x2e+len_name:ofs+0x2e+len_name+len_extra]
    if b'Copy' in filename:
        flag += extra[12:14][::-1]
    ofs += 0x2e+len_name+len_extra

print(flag)
