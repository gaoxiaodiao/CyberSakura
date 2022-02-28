from ptrlib import *
import string
table = string.ascii_uppercase

def calc_hash(name, key):
    hashval = 0
    for c in name:
        hashval = ((ord(c) | 0x20) + ror(hashval, 8, bits=32)) ^ key
    return hashval

for pattern in brute_force_attack(6, table_len=len(table)):
    data = brute_force_pattern(pattern, table)
    flag = data[:3] + "_" + data[3:] + "FOXY_FOX"
    if calc_hash(flag, 0x7C35D9A3) == 0xf92ac34:
        print(flag)
        break
