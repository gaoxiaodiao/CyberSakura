from ptrlib import *
import glob
import hashlib
import re
import string

def reverse(h):
    for i in range(10000):
        if hashlib.md5(str2bytes(str(i))).hexdigest() == h:
            return i

def correct(h, contents):
    for c in string.ascii_letters + string.digits + "{}":
        tmp = contents + c
        if hashlib.md5(str2bytes(tmp)).hexdigest() == h:
            return c
    return '?'

badguy = []
for path in glob.glob("records/*.txt"):
    with open(path, "r") as f:
        contents = ""
        for line in f:
            if "Hash" not in line:
                contents += line
            else:
                h = re.findall("Hash: ([0-9a-f]+)", line)[0]
        if h != hashlib.md5(str2bytes(contents)).hexdigest():
            w = re.findall("report-([0-9a-f]+).txt", path)[0]
            c = correct(h, contents)
            badguy.append((reverse(w), c))

for item in sorted(badguy, key=lambda x:x[0]):
    print(item[1], end="")
