#!/usr/bin/env python2


import string

from crypto_commons.generic import chunk_with_remainder
from crypto_commons.netcat.netcat_commons import nc

known = set()
bits = []
while True:
    s = nc("34.107.12.125", 31133)
    s.sendall("GET /404.php HTTP/1.0\r\nHost: aaa\r\n\r\n")
    x = s.recv(9999)
    if "500" in x:
        bits = []
        continue
    else:
        print(bits)
    print(x)
    if x not in known:
        known.add(x)
        if "1.0" in x:
            bits.append(0)
        else:
            bits.append(1)
    s.close()

offset = 0
real_bits = []
counter = 0
prev = bits[0]
for bit in bits:
    if bit != prev:
        if counter % 3 == 1:
            counter -= 1
        elif counter % 3 == 2:
            counter += 1
        for _ in range(counter / 3):
            real_bits.append(prev)
        counter = 1
    else:
        counter += 1
    prev = bit
print(real_bits)

chunks = chunk_with_remainder(real_bits[offset:], 8)
res = ""
for chunk in chunks:
    c = chr(int("".join(map(str, chunk)), 2))
    if c in string.lowercase or c in string.digits or c in "DCTF{}":
        res += c
    else:
        res += 'X'
print(res)
