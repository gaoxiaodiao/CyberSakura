def decode(data):
    bins = ''
    for c in data:
        bins += str(c & 1)
    return chr(int(bins[::-1], 2))

flag = ''

for x in range(5, 0, -1):
    with open("Item0{}_cp.bmp".format(x), "rb") as f:
        f.seek(0x7e3)
        buf = f.read(40 + 10 * 8)
    j = 0
    for i, c in enumerate(buf):
        if i % 5 == 0:
            flag += decode(buf[j:j+8])
            j += 8
        else:
            j += 1
        if j >= len(buf):
            break

print(repr(flag))
