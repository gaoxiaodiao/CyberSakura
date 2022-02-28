from PIL import Image

# find map
img = Image.open("shuffle_scrambled.png")
mapping = [-1 for i in range(img.size[0])]
for x in range(img.size[0]):
    r, g, b, _ = img.getpixel((x, 0))
    mapping[x] = (g << 8) | r
img.close()

# find key
img = Image.open("black.png")
key = [[] for y in range(img.size[1])]
for y in range(img.size[1]):
    for x in range(100):
        r, g, b, _ = img.getpixel((x, y))
        key[y].append(r)
img.close()

# decrypt
img = Image.open("flag_enc.png")
for y in range(img.size[1]):
    for x in range(img.size[0]):
        r, g, b, _ = img.getpixel((x, y))
        k = key[y][x % len(key[y])]
        r, g, b = r ^ k, g ^ k, b ^ k
        img.putpixel((x, y), (r, g, b))

# unshuffle
img2 = img.copy()
for x in range(img.size[0]):
    for y in range(img.size[0]):
        img2.putpixel(
            (mapping[x], y),
            img.getpixel((x, y))
        )
img2.save("shuffle_scrambled.png")
