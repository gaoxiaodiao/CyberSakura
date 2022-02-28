from ptrlib import xor

with open("nsge", "rb") as f:
    f.seek(0x2004)
    flag = f.read()[:0x18]

flag = xor(flag, "!")
print(flag)
