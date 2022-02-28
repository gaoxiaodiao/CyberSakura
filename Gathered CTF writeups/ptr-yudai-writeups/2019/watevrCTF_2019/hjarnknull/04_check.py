from ptrlib import *
from asm import assemble

sock = Socket("13.48.59.61", 50000)
#sock = Process(["python", "hjarnknull.py"])

# 2
# 0b00000100 10110111 10110001
# 0b00000000 00000001
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
    
    "shl data[1], data[101]",
    "or data[1], data[101]",
    "shl data[1], data[101]",
    "shl data[1], data[101]",
    "shl data[1], data[101]",
    "shl data[1], data[101]",
    "or data[1], data[101]",
    "shl data[1], data[101]",
    "shl data[1], data[101]",
    "shl data[1], data[101]",
    "or data[1], data[101]",
    "shl data[1], data[101]",
    "shl data[1], data[101]",
    "or data[1], data[101]",
    "shl data[1], data[101]",
    "or data[1], data[101]",
    "shl data[1], data[101]",
    "shl data[1], data[101]",
    "or data[1], data[101]",
    "shl data[1], data[101]",
    "or data[1], data[101]",
    "shl data[1], data[101]",
    "shl data[1], data[101]",
    "shl data[1], data[101]",
    "chall data[1]",
    
    "shl data[2], data[101]",
    "shl data[2], data[101]",
    "shl data[2], data[101]",
    "or data[2], data[101]",
    "shl data[2], data[101]",
    "shl data[2], data[101]",
    "or data[2], data[101]",
    "shl data[2], data[101]",
    "or data[2], data[101]",
    "shl data[2], data[101]",
    "shl data[2], data[101]",
    "or data[2], data[101]",
    "shl data[2], data[101]",
    "or data[2], data[101]",
    "shl data[2], data[101]",
    "or data[2], data[101]",
    "shl data[2], data[101]",
    "shl data[2], data[101]",
    "or data[2], data[101]",
    "shl data[2], data[101]",
    "or data[2], data[101]",
    "shl data[2], data[101]",
    "shl data[2], data[101]",
    "shl data[2], data[101]",
    "shl data[2], data[101]",
    "or data[2], data[101]",
    "chall data[2]",

    "recv data[0]",
    "recv data[1]",
    "recv data[2]",
    "shr data[100], data[101]",
    "shl data[102], data[101]",
    "iseq data[0]=data[100] { call code[1] }"
])
for i, code in enumerate(codeList):
    print(code)
    sock.sendline(code)

sock.interactive()
