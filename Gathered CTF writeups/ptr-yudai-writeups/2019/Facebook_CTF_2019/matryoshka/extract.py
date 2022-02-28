#offset = 393216
offset = 424434

with open("pickachu_wut.png", "rb") as f:
    f.seek(offset)
    buf = f.read()

with open("out2", "wb") as f:
    f.write(buf)
