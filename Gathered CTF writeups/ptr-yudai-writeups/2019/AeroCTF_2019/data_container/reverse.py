with open("container", "rb") as f:
    buf = f.read()
with open("output", "wb") as f:
    f.write(buf[::-1])
