from PIL import Image, ImageDraw
import re

with open("data.txt", "r") as f:
    buf = bytes.fromhex(f.read().rstrip())

width, height = 1000, 1000
img = Image.new('RGB', (width, height), (255, 255, 255))
draw = ImageDraw.Draw(img)

# BAR
r = re.findall(b"BAR (\d+), (\d+), (\d+), (\d+)", buf)
for pos in r:
    pos = list(map(int, pos))
    sx, sy, px, py = pos
    #draw.rectangle((width - sx, height - sy, width - (sx + px), height - (sy + py)), fill=(0, 0, 0), outline=(0, 0, 0))
    draw.rectangle((sx, sy, (sx + px), (sy + py)), fill=(0, 0, 0))

# BITMAP
r = re.findall(b"BITMAP (\d+),(\d+),(\d+),(\d+),(\d+),(.+)\r\n", buf)
for bitmap in r:
    x, y, w, h, m, data = bitmap
    x, y, w, h = int(x), int(y), int(w), int(h)
    for i, c in enumerate(data):
        for j in range(8):
            oy = i // w
            ox = (i % w) * 8 + j
            bmp = (c >> (7 - j)) & 1
            if bmp == 0:
                img.putpixel((x + ox, y + oy), (0, 0, 0))
            else:
                img.putpixel((x + ox, y + oy), (255, 255, 255))

img = img.rotate(180)
img.save("result.png")
    
