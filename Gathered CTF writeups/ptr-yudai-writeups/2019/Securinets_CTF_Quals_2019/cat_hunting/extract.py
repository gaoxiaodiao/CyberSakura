offset = 0x1e6171e4
size = 757
#offset = 0x1ebfa19e
#size = 439
offset = 0x1e9d5162
size = 87381
offset = 0x1e63218f
size = 561
offset = 0x1249819e
size = 439
with open("cat_hunting", "rb") as f:
    f.seek(offset)
    buf = f.read(size)

with open("output.gz", "wb") as f:
    f.write(buf)
