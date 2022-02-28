from PIL import Image
from pyzbar.pyzbar import decode

qr = Image.new("RGB", (21, 21), (255, 255, 255))

for i in range(1, 442):
    img = Image.open("frames/{}.png".format(i))
    c = img.getpixel((0, 0))
    x, y = (i - 1) % 21, (i - 1) // 21
    if c[0] == 0:
        qr.putpixel((x, y), (0, 0, 0))
    else:
        qr.putpixel((x, y), (255, 255, 255))

qr = qr.resize((21 * 4, 21 * 4))
print(decode(qr))
