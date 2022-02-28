from ptrlib import *
from asm import assemble

sock = Socket("13.48.59.61", 50000)
#sock = Process(["python", "hjarnknull.py"])

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
    
    "shl data[3], data[101]",
    "or data[3], data[101]",
    "shl data[3], data[101]",
    "or data[3], data[101]",
    "shl data[3], data[101]",
    "chall data[3]"
])
for i, code in enumerate(codeList):
    print(code)
    sock.sendline(code)

sock.interactive()
