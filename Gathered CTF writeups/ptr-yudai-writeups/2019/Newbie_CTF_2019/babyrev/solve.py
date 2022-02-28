"""
for i in range(size):
    c = buf[i]
    enc += table[(c // 10) * 16 + c % 10]
"""
with open("babyrev.exe", "rb") as f:
    f.seek(0x8fb0)
    table = f.read(0x100)

with open("enc.txt", "rb") as f:
    cipher = f.read()

flag = ""
for i, c in enumerate(cipher):
    for x in range(0x100):
        if table[(x // 10) * 16 + (x % 10)] == c ^ (0x16 - (i%2)):
            flag += chr(x)
            break

print(flag)
