from PIL import Image

img_orig = Image.open("original.png")
img_enc = Image.open("encrypted.png")

f = lambda x, y: (x - y) % 0x100

size = img_orig.size
for y in range(size[1]):
    for x in range(size[0]):
        c1 = img_orig.getpixel((x, y))
        c2 = img_enc.getpixel((x, y))
        r, g, b = f(c1[0], c2[0]), f(c1[1], c2[1]), f(c1[2], c2[2])
        img_orig.putpixel((x, y), (r, g, b, 255))

img_orig.save("hoge.png")
