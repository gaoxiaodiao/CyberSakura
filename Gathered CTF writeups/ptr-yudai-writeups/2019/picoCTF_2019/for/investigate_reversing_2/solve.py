with open("encoded.bmp", "rb") as f:
    f.seek(0x7d0)
    buf = f.read(0x32 * 8)

flag = ''
bin_flag = ''
for i, c in enumerate(buf):
    bin_flag += str(c & 1)
    if i % 8 == 7:
        flag += chr(int(bin_flag[::-1], 2) + 5)
        bin_flag = ''

print(repr(flag))
