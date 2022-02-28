import re

r = "a*(b+a+)*b*aba|b+a*(b+a+)*b*aba"

for line in open("yay.txt", "r"):
    x = line.strip()
    if not re.match(r, x):
        print("YAY: " + x)
        exit()

for line in open("nay.txt", "r"):
    x = line.strip()
    if re.match(r, x):
        print("NAY: " + x)
        exit()
