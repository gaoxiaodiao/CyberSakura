#!/usr/bin/env python
import sys
import pickle
from PIL import Image
from captcha import erode

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: {} <captcha.png> <answer>".format(sys.argv[0]))
        exit()
    try:
        with open("char.db", "rb") as f:
            pattern = pickle.load(f)
    except:
        pattern = {}

    img = erode(Image.open(sys.argv[1]).convert('L'))
    
    assert len(sys.argv[2]) == 5
    assert img.size == (200, 50)

    for i, c in enumerate(sys.argv[2]):
        dotset = set()
        for y in range(50):
            for x in range(40):
                col = img.getpixel((i*40 + x, y))
                if col == 0:
                    dotset.add((x, y))
        if c in pattern:
            pattern[c] = pattern[c].intersection(dotset)
        else:
            pattern[c] = dotset

    with open("char.db", "wb") as f:
        pickle.dump(pattern, f)

    print(pattern.keys())
