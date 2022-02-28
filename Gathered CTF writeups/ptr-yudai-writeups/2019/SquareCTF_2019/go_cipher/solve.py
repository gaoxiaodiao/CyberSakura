from z3 import *
from ptrlib import p64

plaintext = open("story4.txt", "rb").read()
encrypted = bytes.fromhex(open("story4.txt.enc").read())
keysum, ciphertext = encrypted[:16], encrypted[16:]

key1, key2, key3 = BitVec("Key1", 64), BitVec("Key2", 64), BitVec("Key3", 64)
solver = Solver()
for i in range(len(plaintext)):
    solver.add(
        ciphertext[i] == ((plaintext[i] - (key1 & 0xff)) & 0xff) ^ (key2 & 0xff) ^ (key3 & 0xff)
    )
    key1 = RotateRight(key1, 1)
    key2 = RotateLeft(key2, 1)
    key3 = RotateLeft(key3, 1)

r = solver.check()
if r == sat:
    m = solver.model()
    print(m)
    for d in m.decls():
        if d.name() == 'Key1':
            key1 = p64(m[d].as_long())
        elif d.name() == 'Key2':
            key2 = p64(m[d].as_long())
        elif d.name() == 'Key3':
            key3 = p64(m[d].as_long())
with open("key", "wb") as f:
    f.write(key1 + key2 + key3)
