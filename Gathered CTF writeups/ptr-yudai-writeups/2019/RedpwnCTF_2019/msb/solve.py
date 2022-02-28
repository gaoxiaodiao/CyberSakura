from PIL import Image

img = Image.open("lol.png")

bits = ""
for x in range(img.size[0]):
    for y in range(img.size[1]):
        r, g, b, _ = img.getpixel((x, y))
        bits += str(b >> 7)
        #print(r >> 7, g >> 7, b >> 7)
    x = bytes.fromhex(hex(int(bits, 2) << 6)[2:])
    print(x)
    exit()
