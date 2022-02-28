with open("mystery.png", "rb") as f:
    buf1 = f.read()[-0x10:]
with open("mystery2.png", "rb") as f:
    buf2 = f.read()[-2:]
with open("mystery3.png", "rb") as f:
    buf3 = f.read()[-8:]

flag = [0 for i in range(0x1a)]
flag[1] = buf3[0]
flag[0] = buf2[0] - ((0x2a + (0x2a >> 7)) >> 1)
flag[2] = buf3[1]
flag[4] = buf1[0]
flag[5] = buf3[2]
for i in range(4):
    flag[6 + i] = buf1[1 + i]
flag[3] = buf2[1] - 4
for i in range(5):
    flag[0x0a + i] = buf3[3 + i]
for i in range(0xf, 0x1a):
    flag[i] = buf1[1 + 4 + i - 0xf]
for c in flag:
    print(chr(c), end="")
