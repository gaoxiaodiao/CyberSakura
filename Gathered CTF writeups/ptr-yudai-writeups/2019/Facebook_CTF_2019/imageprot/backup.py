with open("pon", "rb") as f:
    buf = f.read()

#key = b'\n    -=[ teapot ]=-\n\n ??    _...._\n  '

data  = "ff d8 ff e0 00 10 4a 46  49 46 00 01 01 00 00 48"
data += "00 48 00 00 ff e1 04 dc  45 78 69 66 00 00 4d 4d"
data = bytes.fromhex(data.replace(" ", ""))

key = b''
for a, b in zip(buf[:len(data)], data):
    key += bytes([a^b])
print(key)

for i in range(len(buf)):
    buf = buf[:i] + bytes([buf[i] ^ key[i % len(key)]]) + buf[i+1:]

with open("out", "wb") as f:
    f.write(buf)
