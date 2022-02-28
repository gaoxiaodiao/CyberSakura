from ptrlib import *
import base64
from bls.scheme import *
from bplib.bp import G1Elem, G2Elem
from petlib.bn import Bn
from bls.utils import *

def my_aggregate_vk(params, vk, threshold=True):
    (G, o, g1, g2, e) = params
    t = len(vk)
    l = [lagrange_basis(t, o, i, 0) for i in range(1,t+1)] if threshold else [1 for _ in range(t)]
    # aggregate keys
    aggr_vk = ec_sum([l[i]*vk[i] for i in range(t)])
    return aggr_vk
"""
def sign(data, pvks):
    sock.sendlineafter("flag\x0d\n", "3")
    sock.recvline()
    sock.sendline(data)
    sock.recvline()
    return base64.b64decode(sock.recvline())
"""

# from server
params = setup()
G, o, g1, g2, e = params
(sks, vks) = ttp_keygen(params, 2, 3)

# calc p2
p0 = vks[0]
p1 = vks[1]
l = [lagrange_basis(3, o, i, 0) for i in range(1, 4)]
P = G.hashG1(b"this stuff")
p2 = (l[0] * p0).neg() + (l[1] * p1).neg()
aggr_vk = aggregate_vk(params, [p0, p1, p2])
print(G.pair(P, aggr_vk).export())

# calc s1, s2
l = [lagrange_basis(2, o, i, 0) for i in range(1, 3)]
print(l)
s0 = l[1] * sign(params, sks[0], b"ham")
s1 = l[0] * s0
sigma = aggregate_sigma(params, [s0, s1])
print(G.pair(sigma, g2).export())

# verify
print(verify(params, aggr_vk, sigma, b"this stuff"))
