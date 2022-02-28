from PIL import Image

img = Image.open("logo.png")

result = ""
for y in range(9):
    for x in range(img.size[0]):
        pix = img.getpixel((x, y))
        r = pix[0] & 1
        g = pix[1] & 1
        b = pix[2] & 1
        result += str(r) + str(g) + str(b)

result += "0" * 3
print(hex(int(result, 2))[2:])
print(bytes.fromhex(hex(int(result, 2))[2:]))
