with open("REC.exe", "rb") as f:
    buf = b"MZ" + f.read()

with open("hoge.exe", "wb") as f:
    f.write(buf)
