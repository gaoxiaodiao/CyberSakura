from ptrlib import *
from EllipticCurve import *
import re
import string

sock = Socket("prob.vulnerable.kr", 20016)

# y^2 = x^3 + Ax + B (over N)
x = re.findall(b" (\d+)\*x \+ (\d+), r: (\d+)", sock.recvline())
A, B, r = int(x[0][0]), int(x[0][1]), int(x[0][2])
sock.recvline()
# e
x = re.findall(b"e: \((\d+), (\d+)\)", sock.recvline())
ex, ey = int(x[0][0]), int(x[0][1])
sock.recvline()
# N
N = (int(sock.recvline()[3:]))
sock.recvline()
# C
x = re.findall(b"C: \((\d+), (\d+)\)", sock.recvline())
Cx, Cy = int(x[0][0]), int(x[0][1])
sock.recvline()

F = FiniteField(N)
E = EllipticCurve(F, (A, B))
e = Point(E, ex, ey)
C = Point(E, Cx, Cy)
print(E)
print(e)
print(C)

for d in range(0x1000):
    w = e * d * (r + 1)
    M = C + Point(E, w.x, N - w.y)
    l1 = M.x.bit_length() + (8 - (M.x.bit_length() % 8))
    l2 = M.y.bit_length() + (8 - (M.y.bit_length() % 8))
    x = int.to_bytes(M.x, byteorder='big', length=l1 // 8)
    y = int.to_bytes(M.y, byteorder='big', length=l2 // 8)
    if consists_of(x, string.printable, per=0.8):
        print(x)
        print(y)
    if consists_of(y, string.printable, per=0.8):
        print(x)
        print(y)

sock.close()

