with open("chall.png", "rb") as f:
    buf = f.read()

result = b''
key = b"invisible"
for i, c in enumerate(buf):
    result += bytes([c ^ key[i % len(key)]])

with open("out.png", "wb") as f:
    f.write(result)
