with open("mystery.png", "rb") as f:
    flag = f.read()[-0x1a:]

for i in range(0x06, 0x0f):
    flag = flag[:i] + bytes([flag[i] - 5]) + flag[i+1:]
flag = flag[:0x0f] + bytes([flag[0x0f] + 3]) + flag[0x10:]
print(flag)
