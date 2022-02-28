from ptrlib import ror

hashval = [
    0x13e0ff2c,
    0xB7D26563,
    0x5B9E4069,
    0x98AE69CB,
    0x96AE69D0,
    0x998802F1,
    0x7F3EECA7
]

def calc_hash(name, key):
    hashval = 0
    for c in name:
        hashval = ((ord(c) | 0x20) + ror(hashval, 8, bits=32)) ^ key
    return hashval

with open("apilist_kernel32", "r") as f:
    for line in f:
        for h in hashval:
            if calc_hash(line.strip(), 0x7C35D9A3) == h:
                print(hex(h), line.strip())
                break
