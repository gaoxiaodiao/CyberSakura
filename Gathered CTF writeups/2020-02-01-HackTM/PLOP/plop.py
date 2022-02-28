from z3 import *
import binascii

s = Solver()

a = BitVec('a', 64)
b = BitVec('b', 64)
c = BitVec('c', 64)
d = BitVec('d', 64)
e = BitVec('e', 64)
f = BitVec('f', 64)
g = BitVec('g', 64)
i = BitVec('i', 64)

t = RotateLeft(a, 0xe) ^ 0xdc3126bd558bb7a5
s.add(b == RotateRight(t ^ 0x76085304e4b4ccd5, 0x28))
h = RotateLeft(b, 0x28) ^ 0x76085304e4b4ccd5
s.add(RotateLeft(c, 0x3e) ^ 0x1cb8213f560270a0 == h)
s.add(RotateLeft(d, 2) ^ 0x4ef5a9b4344c0672 == h)
s.add(e == RotateRight(h ^ 0xe28a714820758df7, 0x2d))
h = RotateLeft(e, 0x2d) ^ 0xe28a714820758df7
s.add(RotateLeft(f, 0x27) ^ 0xa0d78b57bae31402 == h)
v = 0x4474f2ed7223940
v = ((v << 0x35) | (v >> (64-0x35))) & 0xffffffffffffffff
s.add(RotateRight(v ^ g, 0x35) == h)
s.add(RotateRight(h^0xb18ceeb56b236b4b, 0x19) == i)
h = RotateLeft(i, 0x19) ^ 0xb18ceeb56b236b4b

s.add(Extract(7,0,a) == ord('H'))
s.add(Extract(15,8,a) == ord('a'))
s.add(Extract(23,16,a) == ord('c'))
s.add(Extract(31,24,a) == ord('k'))
s.add(Extract(39,32,a) == ord('T'))
s.add(Extract(47,40,a) == ord('M'))
s.add(Extract(55,48,a) == ord('{'))
s.add(Extract(63,56,a) == ord('P'))

def pp(t):
    return binascii.unhexlify(hex(t)[2:].zfill(16))[::-1]

s.check()
m = s.model()

print(b''.join([pp(m[x].as_long()) for x in [a,b,c,d,e,f,g,i]]))