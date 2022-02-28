with open("hb", "rb") as f:
    hb = f.read(0x100000)

ofs = 0
with open("joshua.img", "rb") as f:
    while True:
        buf = f.read(len(hb))
        if buf == b'': break
        x = buf.find(hb[512:0x1000])
        if x >= 0:
            print(hex(ofs + x - 512))
        ofs += len(buf)
