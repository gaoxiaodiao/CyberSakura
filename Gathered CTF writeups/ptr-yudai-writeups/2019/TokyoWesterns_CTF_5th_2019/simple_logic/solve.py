import re

def encrypt(msg, key):
    enc = msg
    mask = (1 << 128) - 1
    for i in range(765):
        enc = (enc + key) & mask
        enc = enc ^ key
    return enc

def decrypt(msg, key):
    enc = msg
    mask = (1 << 128) - 1
    for i in range(765):
        enc = enc ^ key
        enc = (enc - key) & mask
    return enc

def find_next(target, real_key):
    candidate = None
    #print(hex(real_key))
    if target == 16:
        yield real_key
    for pair in pairs:
        mask = 0xff << (target * 8)
        loc_cand = set()
        for c in range(0x100):
            key = real_key | (c << (target * 8))
            y = encrypt(pair[0], key)
            if y & mask == pair[1] & mask:
                loc_cand.add(c)
        if candidate is None:
            candidate = loc_cand
        else:
            candidate &= loc_cand
    if candidate:
        for piece in candidate:
            for x in find_next(target + 1, real_key | piece << (target * 8)):
                yield x

pairs = []
with open("output", "r") as f:
    for line in f:
        r = re.findall("plain=([0-9a-f]+) enc=([0-9a-f]+)", line)
        if r:
            pairs.append((int(r[0][0], 16), int(r[0][1], 16)))

enc = 0x43713622de24d04b9c05395bb753d437
for x in find_next(0, 0):
    msg = decrypt(enc, x)
    print("TWCTF{" + hex(msg)[2:] + "}")
    break
