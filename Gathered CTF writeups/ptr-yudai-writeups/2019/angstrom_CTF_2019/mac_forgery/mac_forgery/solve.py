from ptrlib import *
from Crypto.Util.number import long_to_bytes
from Crypto.Util.strxor import strxor
pad = lambda s, bs: s + (bs - len(s) % bs) * bytes([bs - len(s) % bs])
split = lambda s, n: [s[i:i+n] for i in range(0, len(s), n)]

welcome = b'''\
If you provide a message (besides this one) with
a valid message authentication code, I will give
you the flag.'''

sock = Socket("54.159.113.26", 19002)

# recv
sock.recvuntil("MAC: ")
mac = b''.fromhex(bytes2str(sock.recvline().rstrip()))
iv  = mac[:16]
t   = mac[16:]

m = welcome
m = pad(m, 16)
m = split(m, 16)
m.insert(0, long_to_bytes(len(m), 16))
n = len(m)

# forgery
m += m
m[n] = strxor(strxor(m[n], iv), t)
m.pop(0)

fake_m = b''.join(m)
fake_m = fake_m[:-1] # unpad
fake_iv = strxor(iv, strxor(long_to_bytes(7, 16), long_to_bytes(15, 16)))

sock.recvuntil("Message: ")
sock.sendline(fake_m.hex())
sock.recvuntil("MAC: ")
sock.sendline((fake_iv + t).hex())

sock.interactive()
