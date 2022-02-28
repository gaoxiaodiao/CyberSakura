from ptrlib import *
cipher = ''.join(list(map(chr, [40, 11, 82, 58, 93, 82, 64, 76, 6, 70, 100, 26, 7, 4, 123, 124, 127, 45, 1, 125, 107, 115, 0, 2, 31, 15])))
test = b'cybrics{'

key = xor(test, cipher)

print(xor(cipher, key))
