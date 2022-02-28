# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (default, Oct  7 2019, 17:36:04) 
# [GCC 8.3.0]
# Embedded file name: ./encoder.py
# Compiled at: 2019-10-10 14:14:05
import base64, string, sys
from random import shuffle

def encode(f, inp):
    s = string.printable
    init = lambda : (list(s), [])
    bag, buf = init()
    for x in inp:
        if x not in s:
            continue
        while True:
            r = bag[0]
            bag.remove(r)
            diff = (ord(x) - ord(r) + len(s)) % len(s)
            print(bag)
            if diff == 0 or len(bag) == 0:
                shuffle(buf)
                f.write(('').join(buf))
                f.write('\x00')
                bag, buf = init()
                shuffle(bag)
            else:
                break

        buf.extend(r * (diff - 1))
        f.write(r)

    shuffle(buf)
    f.write(('').join(buf))


if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as (r):
        w = open(sys.argv[1] + '.enc', 'wb')
        b64 = base64.b64encode(r.read())
        encode(w, b64)
# okay decompiling encoder.pyc
