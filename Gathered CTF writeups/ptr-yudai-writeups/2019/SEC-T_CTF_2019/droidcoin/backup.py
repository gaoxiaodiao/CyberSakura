from ptrlib import *

def key_adjust(key):
    key = key[:0xf] + bytes([key[0xf] ^ 0x42])
    return key

def decrypt(enc_cnf, cnf_len, key, key_len):
    table = [0 for i in range(0x100)]
    loopKey = [0 for i in range(0x100)]
    for i in range(0x100):
        table[i] = i;
        loopKey[i] = key[i % key_len]
    x = 0
    for i in range(0x100):
        x = (x + table[i] + loopKey[i]) & 0xff
        table[x], table[i] = table[i], table[x]
    x, y = 0, 0
    for i in range(cnf_len):
        y = (y + 1) & 0xff
        x = (x + table[y]) & 0xff
        table[x], table[y] = table[y], table[x]
        ofs = (table[x] + table[y]) & 0xff
        output += bytes([enc_cnf[i] ^ table[ofs]])
    return output

cnf_len = 0x81
with open("libnative-lib.so", "rb") as f:
    f.seek(0xd84)
    enc_cnf = f.read(cnf_len)

key_len = 0x10
tbl = "abcdefghijklmnopqrstuvwxyz"

for pattern in brute_force_attack(4, table_len=len(tbl)):
    prefix = brute_force_pattern(pattern, table=tbl)
    key = str2bytes(prefix) + b'0STEALCOINZ!'
    output = decrypt(enc_cnf, cnf_len, key, key_len)
    if b'flag' in output or b'\x00f\x00l\x00a\x00g' in output:
        print(output, key)
