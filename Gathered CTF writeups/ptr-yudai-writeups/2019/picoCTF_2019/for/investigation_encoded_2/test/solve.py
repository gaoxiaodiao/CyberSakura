import os

table = "abcdefghijklmnopqrstuvwxyz0123456789 "
for c in table:
    with open("flag.txt", "w") as f:
        f.write("t1m3f1i350000000000044f90727")
    os.system("./mystery")
    with open("output", "rb") as f:
        buf = f.read()
        print(buf)
    break
