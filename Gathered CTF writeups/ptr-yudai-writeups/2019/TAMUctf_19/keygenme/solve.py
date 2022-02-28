import string

def enc(s):
    length = len(s)
    magic = 0x48
    encoded = ''
    for i in range(length):
        x = magic * (ord(s[i]) + 0xC) + 0x11
        x &= 0xffffffff
        y = (x * 0xEA0EA0EB) >> 32
        z = (y >> 6) - (x >> 0x1f)
        w = x - ((z * 0x46) & 0xffffffff) + 0x30
        encoded += chr(w & 0xFF)
        magic = ord(encoded[-1])
    return encoded

encoded = "[OIonU2_<__nK<KsK"
password = ""
for i, c in enumerate(encoded):
    for x in string.printable:
        if enc(password + x) == encoded[:i + 1]:
            password += x
            break
    else:
        print("Something is wrong...", password)
        break

print(password)
print(enc(password))

from ptrlib import *

sock = Socket("rev.tamuctf.com", 7223)
sock.sendline(password[:-1])
sock.interactive()
