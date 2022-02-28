from ptrlib import xor

with open("easy_crackme", "rb") as f:
    f.seek(0x2008)
    flag = f.read(0x2e - 0x08)

flag = xor(flag, bytes([len(flag)]))
print(flag)
