from ptrlib import *

with open("mystery", "rb") as f:
    buf = f.read()

table = []
matrix = []
for i in range(0, 26*8, 8):
    matrix.append(u32(buf[0xdc0 + i:0xdc0 + i + 4]))
    table.append(u32(buf[0xdc4 + i:0xdc4 + i + 4]))

print(table[ord('p') - ord('a')])
print(matrix[ord('p') - ord('a')])

