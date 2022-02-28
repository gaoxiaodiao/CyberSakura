import struct

with open("ScrambleMeBack", "rb") as f:
    table = []
    f.seek(0xdf5e0)
    for i in range(0x60):
        table.append(struct.unpack('<I', f.read(4))[0])

def scramble(key):
    w = 0
    j = 1
    output = b''
    for i in range(2, len(key)):
        j = (key[i] + j * (j + i)) % 0x60 + j
        if i > 8 and i < len(key) - 3:
            v13 = 0x60 * (j // 0x60)
            output += bytes([table[j - v13]])
            w += 1
    return output

def search(key, i=2, j=1, w=0, output=b''):
    if w == len(answer):
        yield key, output
    else:
        if i > 8 and i < len(key) - 3:
            for x in range(0x30, 0x7f):
                try_j = (x + j * (j + i)) % 0x60 + j
                v13 = 0x60 * (try_j // 0x60)
                if len(table) <= try_j - v13:
                    continue
                elif table[try_j - v13] == answer[w]:
                    next_key = key[:i] + bytes([x]) + key[i+1:]
                    for candidate in search(next_key, i+1, try_j, w+1, output+bytes([table[try_j-v13]])):
                        yield candidate
        else:
            next_j = (key[i] + j * (j + i)) % 0x60 + j
            for candidate in search(key, i+1, next_j, w, output):
                yield candidate

answer = b'g0l4n6_15_g00d'
key = b'0' * (8 + 4 + len(answer))

for candidate in search(key):
    print(candidate)
    print(scramble(candidate[0]))
    exit()
