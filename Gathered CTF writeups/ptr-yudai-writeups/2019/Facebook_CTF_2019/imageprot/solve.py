with open("pon", "rb") as f:
    buf = f.read()

with open("key", "rb") as f:
    key = f.read()

for i in range(len(buf)):
    buf = buf[:i] + bytes([buf[i]^key[i%len(key)]]) + buf[i+1:]

with open("out", "wb") as f:
    f.write(buf)
