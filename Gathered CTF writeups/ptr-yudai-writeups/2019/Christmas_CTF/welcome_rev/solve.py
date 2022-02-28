import struct

table = []

def search_by_msb(msb):
    for i, value in enumerate(table):
        if value >> 24 == msb:
            return i, value
    raise Exception("Not found")

def decode(encoded):
    output = ''
    dList = [0, 0, 0, 0]
    for i in range(4):
        d, t = search_by_msb(encoded >> 24)
        dList[3 - i] = d
        encoded = (encoded ^ t) << 8
    encoded = 0xffffffff
    for i in range(4):
        c = dList[i] ^ (encoded & 0xff)
        encoded = (encoded >> 8) ^ table[dList[i]]
        output += chr(c)
    return output

if __name__ == '__main__':
    with open('welcome_rev', 'rb') as f:
        f.seek(0xae0)
        for i in range(0x100):
            table.append(struct.unpack('<I', f.read(4))[0])
    with open('encrypted', 'rb') as f:
        output = ''
        while True:
            data = f.read(4)
            if data == b'': break
            v = decode(struct.unpack('<I', data)[0])
            output += v
        print(output)
