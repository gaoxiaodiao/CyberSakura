from ptrlib import *
import os
import hashlib
from PIL import Image

img = Image.new('RGB', (600, 267))

for x in range(600):
    path = hashlib.md5(str2bytes(str(x))).hexdigest() + ".png"
    if os.path.exists("parts/parts/" + path):
        target = Image.open("parts/parts/" + path)
        for y in range(img.size[1]):
            img.putpixel((x, y), target.getpixel((0, y)))

img.save("image.png")
