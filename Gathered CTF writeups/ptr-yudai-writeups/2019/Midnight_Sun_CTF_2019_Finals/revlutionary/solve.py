with open("dump.bin", "rb") as f:
    data = f.read()

flag = ""
start = 0xd47d
while not flag.startswith("midnight"):
    print(hex(start))
    flag = chr(start & 0xff) + flag
    next_chr = start >> 8
    c = 0
    while data.find(next_chr, c) != -1:
        start = data.find(next_chr)
        c = start + 1
    print(flag)
