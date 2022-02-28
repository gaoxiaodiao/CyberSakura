import hashlib
import base64
fake_msg = '{"command": "flag", "params": {"name": "fbctf"}}'

n = int(raw_input("n = "))
A = int(raw_input("A = "))
B = int(raw_input("B = "))
s = int(raw_input("s = "))
r = int(raw_input("r = "))
Gx = int(raw_input("Gx = "))
Gy = int(raw_input("Gy = "))
Hx = int(raw_input("Hx = "))
Hy = int(raw_input("Hy = "))

F = Zmod(n)
E = EllipticCurve(F, [A, B])
G = E.point((Gx, Gy))
H = E.point((Hx, Hy))

k = n - 314
Q = G * k
r = int(hashlib.sha256(fake_msg + str(Q[0])).hexdigest(), 16)
pub = discrete_log(H, G, operation='+')
assert r * H == pub * r * G
s = (k - pub * r) % E.order()
sig = base64.b64encode(str(r) + "|" + str(s))

print(pub)
print(Q)
print(s*G + r*H)
print(sig)
