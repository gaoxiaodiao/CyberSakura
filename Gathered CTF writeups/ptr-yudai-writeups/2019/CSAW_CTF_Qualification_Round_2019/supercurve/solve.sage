p = 14753
E = EllipticCurve(FiniteField(p), [1, -1])
P = E.point((1056, 4119))
G = E.point((1, 1))
x = G.discrete_log(P)
print(x)
