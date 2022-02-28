from ptrlib import *
import string
table = string.ascii_letters + string.digits

def calc_hash(name, key):
    hashval = 0
    for c in name:
        hashval = ((ord(c) | 0x20) + ror(hashval, 8, bits=32)) ^ key
    return hashval

for pattern in brute_force_attack(4, table_len=len(table)):
    password = brute_force_pattern(pattern, table)
    if calc_hash(password, 0x7C35D9A3) == 0x8faf5559:
        print(password)
        break
