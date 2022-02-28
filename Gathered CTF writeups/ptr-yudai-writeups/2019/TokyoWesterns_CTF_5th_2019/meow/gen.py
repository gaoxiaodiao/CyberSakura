from PIL import Image

img = Image.new("RGB", (768, 768), (255, 255, 255))

for x in range(img.size[0]):
    for y in range(img.size[1]):
        img.putpixel((x, y), (x & 0xff, x >> 8, x & 0xff))

img.save("shuffle_original.png")

import os
os.system("neko meow.n shuffle_original.png shuffle_enc.png")

# find key
img = Image.open("black.png")
key = [[] for y in range(img.size[1])]
for y in range(img.size[1]):
    for x in range(100):
        r, g, b, _ = img.getpixel((x, y))
        key[y].append(r)
img.close()

# decrypt
img = Image.open("shuffle_enc.png")
for y in range(img.size[1]):
    for x in range(img.size[0]):
        r, g, b, _ = img.getpixel((x, y))
        k = key[y][x % len(key[y])]
        r, g, b = r ^ k, g ^ k, b ^ k
        img.putpixel((x, y), (r, g, b))

img.save("shuffle_scrambled.png")
