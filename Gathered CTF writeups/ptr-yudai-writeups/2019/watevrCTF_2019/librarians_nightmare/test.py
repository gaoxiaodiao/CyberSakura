from ptrlib import inverse

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_'
a = 0xdeadbeef
k = 0xcafebabe
m = 4902227890643
c = 0xc0beb33f
d = inverse(c, m)

def f(n):
    if n == 0:
        return (c + k) % m
    if n % 2 == 0:
        fx = f(n // 2)
        return (k + (fx ** 2 - 2 * k * fx + k ** 2) * d) % m
    else:
        fx = f((n - 1) // 2)
        return (k + a * (fx ** 2 - 2 * k * fx + k ** 2) * d) % m

def ff(n):
    return (pow(a, n) * c + k) % m
    
def n2st(n, length = 7):
    if length == 0:
        return ""
    ch = chars[n % len(chars)]
    return n2st(n // len(chars), length - 1) + ch

for i in range(10):
    print(f(i), ff(i))
