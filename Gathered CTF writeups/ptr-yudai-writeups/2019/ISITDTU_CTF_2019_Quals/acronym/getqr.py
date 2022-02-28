from PIL import Image

img = Image.open("qr.png")

output = ""
for y in range(83, 256, 7):
    for x in range(155, 330, 7):
        if img.getpixel((x, y))[0] == 0:
            output += "X"
        else:
            output += "_"
    output += "\n"
    
print(output)
