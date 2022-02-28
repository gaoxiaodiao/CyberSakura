import math
import string
import base64

with open("cipher.txt") as f:
    buf = f.read()

table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
nlist = map(int, buf[1:-1].split(","))
flag = ""
for n in nlist:
    x = int(math.log2(n))
    flag += table[x - 1]
print(base64.b64decode(flag))
