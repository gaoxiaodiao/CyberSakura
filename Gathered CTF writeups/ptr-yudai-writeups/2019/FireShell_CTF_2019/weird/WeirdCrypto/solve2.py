def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
 
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

c = int(open('weird_animal').read().encode('hex'), 16)
p = 1860359276734318356125628767
q = 71875025974474493093168609593879437761722540733233
n = p * q
e = 65537
phi = (p - 1) * (q - 1)
 
d = modinv(e, phi)
 
m = pow(c, d, n)
print(hex(m)[2:].rstrip('L').decode('hex'))
