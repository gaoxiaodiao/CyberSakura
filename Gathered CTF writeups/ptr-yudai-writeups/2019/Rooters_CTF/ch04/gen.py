with open("hackme_dump.bin", "rb") as f:
    f.seek(0x114c)
    for i in range(0x30):
        f.read(3)
        print("0x{:02x}, ".format(f.read(1)[0]), end="")
