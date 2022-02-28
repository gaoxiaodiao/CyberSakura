from ptrlib import inverse

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_'
    
def n2st(n, length = 7):
    if length == 0:
        return ""
    ch = chars[n % len(chars)]
    return n2st(n // len(chars), length - 1) + ch

def st2n(st):
    n = 0
    for i, c in enumerate(st):
        n += 65**(6-i) * chars.index(c)
    return n

m = 4902227890643
f0 = st2n("TgIgMEI")
f1 = st2n("Nh2uPF8")
f2 = st2n("h5EMH{G")

a = ((f1 - f2) * inverse(f0 - f1, m)) % m
c = ((f1 - f0) * inverse(a - 1, m)) % m
k = (f0 - c) % m
d = inverse(c, m)
print("a = {}".format(a))
print("c = {}".format(c))
print("k = {}".format(k))

def ff(n):
    return (pow(a, n, m) * c + k) % m

fn = st2n('watevr{')
b = ((fn - k) * d) % m
print("Solve {} = {} ^ n mod {}".format(b, a, m))

n = 2555482270306
print("P.{} / L.{}".format(n // 100, n % 100))
