def decode(data):
    bins = ''
    for c in data:
        bins += str(c & 1)
    return chr(int(bins[::-1], 2))

with open("encoded.bmp", "rb") as f:
    f.seek(0x2d3)
    buf = f.read(0x32 * 8 + 0x32)

x = 0
flag = ''
for i in range(0x64):
    if i % 2 == 0:
        flag += decode(buf[x:x+8])
        x += 8
    else:
        x += 1
print(flag)
