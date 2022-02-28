with open("output.png", "rb") as f:
    f.seek(0x0084053c)
    buf = b'\x89' + f.read()
with open("hoge.png", "wb") as f:
    f.write(buf)
