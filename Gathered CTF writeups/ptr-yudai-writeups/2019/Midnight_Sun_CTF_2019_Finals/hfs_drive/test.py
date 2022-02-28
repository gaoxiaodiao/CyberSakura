with open("hfs_superdrive", "rb") as f:
    buf = f.read()

with open("superdrive", "wb") as f:
    f.write(buf[0x400:])
