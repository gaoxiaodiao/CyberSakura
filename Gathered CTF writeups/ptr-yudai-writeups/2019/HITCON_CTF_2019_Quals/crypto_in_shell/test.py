from Crypto.Cipher import AES
from ptrlib import *

def encrypt(key, msg):
    return AES.new(key, AES.MODE_CBC, iv=b'\0'*16).encrypt(msg)

def decrypt(key, msg):
    return AES.new(key, AES.MODE_CBC, iv=b'\0'*16).decrypt(msg)

key = b"\xd3\xb16\xda\x18n\x19\xe4\xa5\xdb\x83\xd8\x13\xc52\x07"
r = b'\x00' * 8 + b'\x00' * 16
print(r)
r = encrypt(key, r)
print(r)
