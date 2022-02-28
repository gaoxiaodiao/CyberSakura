with open("VsiMple.exe", "rb") as f:
    f.seek(0x22248)
    buf = f.read(0x100)

flag = ""
ofs = 0
for i in range(0x2a):
    a = buf[ofs]
    b = buf[ofs + 2]
    ofs += 6
    flag += chr(a ^ b)
print(flag)
