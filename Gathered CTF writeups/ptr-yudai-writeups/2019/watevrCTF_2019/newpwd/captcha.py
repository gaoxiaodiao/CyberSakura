#!/usr/bin/env python
from PIL import Image
import pickle
import sys

def erode(img):
    out = Image.new('L', img.size, 255)
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            c = 0
            for j in range(-1, 2):
                for i in range(-1, 2):
                    c += img.getpixel(((x + i)%img.size[0],
                                       (y + j)%img.size[1]))
            if c == 0:
                out.putpixel((x, y), 0)
            else:
                out.putpixel((x, y), 255)
    return out

def recognize(img, pattern):
    img = erode(img)
    assert img.size == (200, 50)
    output = ''
    for i in range(5):
        possible = {}
        for y in range(50):
            for x in range(40):
                col = img.getpixel((i*40+x, y))
                if col != 0: continue
                for c in pattern:
                    if (x, y) in pattern[c]:
                        if c in possible:
                            possible[c] += 1
                        else:
                            possible[c] = 1
        maxCount = 0.0
        maxC = '?'
        #print("=" * 10)
        for c in possible:
            #print(c, possible[c] / len(pattern[c]))
            if maxCount < possible[c] / len(pattern[c]):
                maxC = c
                maxCount = possible[c] / len(pattern[c])
        output += maxC
    return output

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <captcha.png>".format(sys.argv[0]))
        exit()

    with open("char.db", "rb") as f:
        pattern = pickle.load(f)
    img = Image.open(sys.argv[1]).convert('L')
    print(recognize(img, pattern))
