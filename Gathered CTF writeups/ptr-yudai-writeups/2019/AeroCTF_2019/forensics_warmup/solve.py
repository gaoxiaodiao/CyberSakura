from PIL import Image

size = 360000
# w * h = 360000
w = 800
h = size // w
img = Image.new('RGB', (w, h))

with open("just_a_meme", "rb") as f:
    buf = f.read()

x = 0
for i in range(0, len(buf), 3):
    r, g, b = buf[i:i+3]
    img.putpixel((x % w, h - x // w - 1), (r, g, b))
    x += 1

img.save("image.png")
