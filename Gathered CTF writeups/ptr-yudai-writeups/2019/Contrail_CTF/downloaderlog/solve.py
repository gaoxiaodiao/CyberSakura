with open("k7zg2B", "rb") as f:
    binary = f.read()

for i in range(389):
    binary = binary[:0x10d5+i] + bytes([binary[0x10d5+i] ^ 0x19]) + binary[0x10d6+i:]

with open("unpacked", "wb") as f:
    f.write(binary)

# ctrctf{u_are_3inary_4na1yst}
