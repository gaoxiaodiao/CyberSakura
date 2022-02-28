from ptrlib import *
from asm import assemble

sock = Socket("13.48.59.61", 50000)
#sock = Process(["python", "hjarnknull.py"])

# 2
# 0b00000000 00101100
# 0b00010001 11100010
codeList = assemble([
    "iseq data[999]=data[999] { call code[2] }",
    "iseq data[999]=data[999] { call code[1] }", # infinite loop
    "shl data[0], data[101]",
    "shl data[0], data[101]",
    "shl data[0], data[101]",
    "or data[0], data[101]",
    "shl data[0], data[101]",
    "shl data[0], data[101]",
    "or data[0], data[101]",
    "shl data[0], data[101]",
    "or data[0], data[101]",
    "chall data[0]",
    "recv data[0]", # recv inputs
    "recv data[1]",
    "recv data[2]",
    "shr data[10], data[101]", # data[10] = -2 (= 0b11111...1110)
    "not data[10]",
    "shr data[10], data[101]",
    "shl data[10], data[101]", #
    "shr data[1], data[101]",
    "shr data[1], data[101]",
    "shr data[1], data[101]",
    "shr data[1], data[101]",
    "shr data[1], data[101]",
    "shr data[1], data[101]",
    "shr data[1], data[101]",
    "shr data[1], data[101]",
    "shr data[1], data[101]",
    "shr data[1], data[101]",
    "shr data[1], data[101]",
    "shr data[1], data[101]",
    "shr data[1], data[101]",
    "shr data[1], data[101]",
    "or data[1], data[10]", # check the least significant bit
    "not data[1]",
    "iseq data[1]=data[101] { call code[1]}" # if (x>>i)&1==0 --> infinite
])
for i, code in enumerate(codeList):
    print(code)
    sock.sendlineafter(str(i)+": ", code)

sock.interactive()
