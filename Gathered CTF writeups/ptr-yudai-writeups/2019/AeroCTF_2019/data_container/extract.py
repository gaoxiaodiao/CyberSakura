with open("extracted.png", "rb") as f:
    buf = f.read()

signature = b"IEND\xaeB\x60\x82"
ofs = buf.index(signature) + len(signature)
with open("extracted2", "wb") as f:
    f.write(buf[ofs:])
