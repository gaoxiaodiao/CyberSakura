with open("curious", "rb") as f:
    buf = f.read()

key = b"\x13\x37"
result = b''
for i in range(len(buf)):
    result += bytes([key[i % 2] ^ buf[i]])

with open("file", "wb") as f:
    f.write(b'PK' + result[::-1])
