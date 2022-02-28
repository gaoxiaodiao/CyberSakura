from PIL import Image

img1 = Image.open("koala.png")
img2 = Image.open("koala2.png")

for y in range(1):
    for x in range(img1.size[0]):
        pix1 = img1.getpixel((x, y))
        pix2 = img2.getpixel((x, y))
        if pix1 != pix2:
            print(pix1[0] - pix2[0], pix1[1] - pix2[1], pix1[2] - pix2[2])
