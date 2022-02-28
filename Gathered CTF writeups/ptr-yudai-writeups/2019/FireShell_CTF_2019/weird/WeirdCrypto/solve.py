from ptrlib import *

def stoi(s):
    return reduce(lambda x, y: ord(y) + 256 * x, s, 0)
 
pubkey = 'MDwwDQYJKoZIhvcNAQEBBQADKwAwKAIhASefFhHtsI2oAhTr0Bx4XnClvcgyU+2ffBh53kF90egvAgMBAAE='.decode('base64')
pubkey = pubkey[-38:-5]
print(pubkey.encode('hex'))
c = int(open('weird_animal').read().encode('hex'), 16)
n = stoi(pubkey)
print(n)
exit(1)
p = 1860359276734318356125628767
q = 71875025974474493093168609593879437761722540733233
 
e = 0x010001
phi = (p - 1) * (q - 1)
 
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
 
d = modinv(e, phi)
 
m = pow(c, d, n)
print hex(m)[2:-1].decode('hex')
