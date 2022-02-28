# SECCON{379eaX85bTa99c695b36855i4Ycfa5b5}
from ptrlib import u16
from PIL import Image

with open("firmware.bin", "rb") as f:
    f.seek(0x20)
    s = f.read(0x40 * 9)
w = b''.join([bytes([i]) for i in range(0x3f, 0x7f)])

img = Image.new('L', (600, 8 * 13), 255)

offset = 0
dd = 0
delta = 1
x, y = 0, 0
while True:
    try:
        """
        offset = offset + (dd // 6)
        bVar1 = (offset + 0x20) & 0xff
        Z = (offset & 0xff00) | bVar1
        bVar2 = (-(offset & 0xff) - 0x3f)
        Z = ((u16(s[Z-0x20:Z-0x20+2]) >> (bVar1 & 1)) & 0xff) + bVar2 & 0x3f
        """
        bVar2 = -(offset + (dd // 6)) - 0x3f
        Z = s[offset + (dd // 6)] + bVar2 & 0x3f
        #Z = (u16(s[Z >> 1:(Z >> 1) + 2]) >> (bVar1 & 1)) + bVar2 & 0x3f
        #print(Z)
        #Z = (offset & 0xff00) + bVar1
        #Z = ((s[(Z >> 1) >> (bVar1 & 1)]) + bVar2) & 0x3f
    except Exception as e:
        print(e)
        break
    c = dd % 6
    while True:
        c -= 1
        if c < 0: break
        Z >>= 1
    click = Z & 1
    
    for i in range(8):
        img.putpixel((x, y), (click ^ 1) * 255)
        y += delta
    if delta == 1:
        dd += 1
        if dd > 11:
            dd = 11
            delta = -1
            x += 1
            img.putpixel((x, y), (click ^ 1) * 255)
            continue
    else:
        dd -= 1
        if dd < 0:
            dd = 0
            delta = 1
            x += 1
            offset += 2
            img.putpixel((x, y), (click ^ 1) * 255)
            b = 0
            if (offset & 0xff) < 0x43:
                b = 1
            if b + 2 <= (offset >> 8) - (b + 2):
                break

img.resize((1200, 8*13)).save("flag.png")
