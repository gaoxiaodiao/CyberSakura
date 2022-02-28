import os

table = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "

for c in table:
    with open("flag.txt", "w") as f:
        f.write("encodedgrtwasmvwe")
        #f.write("EncodedGrtWasmVwe")
    os.system("./mystery")
    with open("output", "rb") as f:
        if f.read()[-1] == 0x20:
            print(c)
            break
