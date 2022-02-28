from ptrlib import *
import base64
from bls.scheme import *
from bplib.bp import G1Elem, G2Elem
from petlib.bn import Bn
from bls.utils import *

def sign(data):
    sock.sendlineafter("flag\x0d\n", "3")
    sock.recvline()
    sock.sendline(data)
    sock.recvline()
    return base64.b64decode(sock.recvline())

def flag(s0, p0, s1, p1, p2):
    sock.sendlineafter("flag\x0d\n", "4")
    sock.recvline()
    sock.recvline()
    sock.sendline(base64.b64encode(s0.export()))
    sock.recvline()
    sock.sendline(base64.b64encode(p0.export()))
    sock.recvline()
    sock.sendline(base64.b64encode(s1.export()))
    sock.recvline()
    sock.sendline(base64.b64encode(p1.export()))
    sock.recvline()
    sock.sendline(base64.b64encode(p2.export()))
    return

params = setup()
G, o, g1, g2, e = params

sock = Socket("crypto.chal.csaw.io", 1004)

pvks = [None, None, None]
sock.recvuntil("Abraham\x0d\n")
pvks[0] = base64.b64decode(sock.recvline())
sock.recvuntil("Bernice\x0d\n")
pvks[1] = base64.b64decode(sock.recvline())
sock.recvuntil("Chester\x0d\n")
pvks[2] = base64.b64decode(sock.recvline())

# calc p2
p0 = G2Elem.from_bytes(pvks[0], G)
p1 = G2Elem.from_bytes(pvks[1], G)
l = [lagrange_basis(3, o, i, 0) for i in range(1, 4)]
P = G.hashG1(b"this stuff")
p2 = (l[0] * p0).neg() + (l[1] * p1).neg()
aggr_vk = aggregate_vk(params, [p0, p1, p2])
print(G.pair(P, aggr_vk).export())

# calc s0, s1
lx = [lagrange_basis(2, o, i, 0) for i in range(1, 3)]
s0 = lx[1] * G1Elem.from_bytes(sign(b"ponta"), G)
s1 = lx[0] * s0
sigma = aggregate_sigma(params, [s0, s1])
print(G.pair(sigma, g2).export())

flag(s0, p0, s1, p1, p2)

sock.interactive()
