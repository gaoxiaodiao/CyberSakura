table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
flag = [ord("X") for i in range(0x64)]

flag[0] = ord(table[0x1c])
flag[1] = ord(table[0x36])
flag[2] = ord(table[(0x1c + 0x36) >> 2])
flag[10] = flag[2]
flag[3] = 0x6a
flag[4] = flag[0] + 1
for p in [0xc, 0x16, 0x18]:
    flag[p] = flag[4] - 1
flag[6] = flag[3] - 0x20
flag[11] = 0x2f + 1
flag[1 + 0x22] = flag[11] + 9
flag[0x17] = 1 + 0x2f
flag[8] = flag[0] - 1
flag[0x1b] = flag[4] + 2
flag[0x1f] = flag[4] + 2
flag[9] = flag[0x1b] + 7
flag[0x19] = flag[0x1b] + 7
for p in [0xd, 0x11, 0x15]:
    flag[p] = flag[1] + 1
flag[7] = 0x70
flag[0xf] = flag[7] + 3
flag[0xe] = flag[0xf] + 1
flag[0x13] = 0x7a
flag[0x22] = flag[0] - 0x21
flag[0x1a] = 1 + 0x30
flag[0x10] = flag[9] - 0x20
flag[0x1c] = flag[0x10]

flag[0x12] = flag[7] - 0x1e
flag[0x1e] = flag[0x12]

flag[0x20] = flag[4]

#for p in [5, 0x14, 0x1d, 0xc4]:
#    print(flag[p])
print(''.join(list(map(chr, flag))))
