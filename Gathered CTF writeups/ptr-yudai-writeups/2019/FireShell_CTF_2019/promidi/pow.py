import sys
import hashlib
import string
import random

ans = sys.argv[1]
while True:
    text = ''.join([random.choice(string.printable[:-6]) for i in range(8)])
    if hashlib.sha256(text).hexdigest()[-6:] == ans:
        break

print(text)
