with open("hb", "rb") as f:
    header = f.read(0x200)
with open("encrypted.luks", "rb") as f:
    f.seek(0x200)
    buf = f.read()
with open("encrypted.luks", "wb") as f:
    f.write(header + buf)
