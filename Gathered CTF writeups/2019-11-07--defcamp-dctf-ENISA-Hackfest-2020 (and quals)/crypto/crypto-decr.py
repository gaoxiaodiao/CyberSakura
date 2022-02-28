import hashlib
import os
import binascii
def encryptx(data, key):
    encrypted = []
    a, b, c = key
    for d in data:
        keystream = (b & 0xff) ^ (c & 0xff)
        d = (d - (a & 0xff)) ^ keystream
        d = d & 0xff
        encrypted.append(d)
        a = rotr(a)
        b = rotl(b)
        c = rotl(c)
        # print(a, b, c)
    return encrypted
def decrypt(ct):
    key = tuple([BitVec('k%d' % i, 64) for i in range(3)])
    flag = [BitVec('x%d' % i, 64) for i in range(len(ct) / 2)]
    s = Solver()
    for x in flag:
        s.add(x > 0, x < 128)
        s.add(Or(x == 32, x > 32))
    result = encryptx(flag, key)
    for i, x in enumerate(ct.decode("hex")):
        s.add(result[i] == ord(x))
    for i, c in enumerate("Congrats! Flag is: "):
        s.add(flag[i] == ord(c))
    s.check()
    model = s.model()
    solution = [model[x].as_long() for x in flag]
    print("".join(map(chr, solution)))
    return "".join(map(chr, [model[x].as_long() for x in flag]))
ct = 'f59d4ea17bf649c6bf1b3967fe2203b570fd180c4100247847348e20b86c6c7febacc33b5c2f9b8262e40edf114d55286f5d7634735e3671674c5a'
h = ct[:40]
flag = "Congrats! Flag is: DCTF{th1s_w4s_"
for a in range(128):
    for b in range(128):
            for c in range(128):
                data = flag + chr(a) + chr(b) + chr(c) + "}"
                digest = hashlib.sha1(data).hexdigest()
                if digest == h:
                    print(data)