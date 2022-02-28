alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

flag = b64pass
assert alphanumeric.index(flag[0]) == 0x1c
assert alphanumeric.index(flag[0]) + alphanumeric.index(flag[1]) == alphanumeric.index(flag[2])

assert alphanumeric.index(flag[0]) + alphanumeric.index(flag[1]) >> 2 == alphanumeric.index(flag[10])

assert flag[10] == flag[2]

assert alphanumeric.index(flag[1]) == 0x36

assert flag[3] == 0x6a

assert flag[0] + 1 == flag[4]

arr = [0, 0x0c, 0x16, 0x18]
for i in range(4):
    assert flag[arr[i]] == flag[4] - 1

assert flag[11] + 9 == flag[1 + 0x22]

assert flag[3] - 0x20 == flag[6]

assert flag[11] == 1 + 0x2f
assert flag[0x17] == 1 + 0x2f

assert flag[0] - 1 == flag[8]

assert flag[4] + 2 == flag[0x1b]
assert flag[4] + 2 == flag[0x1f]

assert flag[0x1b] + 7 == flag[9]
assert flag[0x1b] + 7 == flag[0x19]

arr = [0xd, 0x11, 0x15]
for i in range(3):
    assert flag[arr[i]] == flag[1] + 1

assert flag[7] == 0x70

assert flag[0xf] == flag[7] + 3

assert flag[0xf] + 1 == flag[0xe]

assert flag[0x13] == 0x7a

assert flag[0] - 0x21 == flag[0x22]

arr = [5, 0x14, 0x1d, 0xc4]
x = 0x58
for i in range(4):
    x ^= flag[arr[i]]
assert x == 0x58

assert flag[0x1a] == 1 + 0x30

assert flag[9] - 0x20 == flag[0x10]
assert flag[0x10] == flag[0x1c]

assert flag[1] == 0x32

assert flag[7] - 0x1e == flag[0x12]
assert flag[0x12] == flag[0x1e]

assert flag[4] == flag[0x20]
