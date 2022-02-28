from ptrlib import *

p = 11
q = 13
d = 113
e = inverse(d, (p-1) * (q-1))

cipher = []
plain = b'give_me_the_flag_please'
for c in plain:
    cipher.append(pow(c, e, p*q))

# 38 118 79 95 127 109 95 127 129 91 95 127 20 114 15 38 127 73 114 95 15 124 95
print(' '.join(list(map(str, cipher))))
