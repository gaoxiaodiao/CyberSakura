import re
import sys
from ptrlib import *

with open(sys.argv[1], "r") as f:
    instList = []
    for line in f:
        r = re.findall("[0-9a-f]{2}\t(.+) (R\d), (.+)", line)
        if r:
            instList.append(r[0])

regs = [0 for i in range(7)]
regs[0] = int(instList[0][2], 16)
for i, inst in enumerate(instList):
    if inst[1] != 'R1': continue
    # for R1
    ope = inst[0]
    src = int(inst[2][1]) - 1
    # past
    if src != 0:
        for j in range(i, len(instList)):
            if instList[j][0] == 'MOVIqq' and instList[j][1] == 'R'+str(src + 1):
                regs[src] = int(instList[j][2], 16)
                break
            elif instList[j][0] == 'MOVIqd' and instList[j][1] == 'R'+str(src + 1):
                regs[src] = int(instList[j][2], 16)
                break
    # do it
    if ope == 'SUB':
        regs[0] = (regs[0] + regs[src]) % (1 << 64)
    elif ope == 'ADD':
        regs[0] = (regs[0] - regs[src]) % (1 << 64)
    elif ope == 'XOR':
        regs[0] ^= regs[src]
    elif ope == 'NEG':
        regs[0] ^= ((1 << 64) - 1)
        regs[0] = (regs[0] + 1) % (1 << 64)
    elif ope == 'NOT':
        regs[0] ^= ((1 << 64) - 1)
    elif ope == 'OR':
        if instList[i+2][0] == 'MOVIqw':
            size = int(instList[i+2][2], 16)
        elif 'MOVIq' in instList[i+1][0]:
            x = int(instList[i+1][2], 16)
            #print("--------")
            #print(hex(regs[0]))
            print(hex(x))
            #print(bin(x))
            #print(bin(regs[0] & x))
            assert regs[0] & x == x
            # for ayaC_3.txt
            #if x != 4 and x != 0x8000000:
            #    regs[0] ^= x
            # for ayaC_4.txt
            #"""
            if x == 0x40201003000:
                #x = 0x40201000000
                x = 0x40001001000
            elif x == 0x2410804000000:
                x = 0x2410804000000
            elif x ==0x10040908000:
                x = 0x10040908000
            elif x == 0x1000008004050:
                x = 0x1000008004010
            elif x == 0x1000b00000000200:
                x = 0x1000b00000000200
            elif x == 0x800000001042:
                x = 0x800000001042
            #"""
            regs[0] ^= x
            continue
        else:
            print(i, instList[i+0])
            print(i, instList[i+1])
            print(i, instList[i+2])
            print(i, instList[i+3])
            print("wOA!?")
            exit(1)
        if instList[i+1][0] == 'SHL':
            regs[0] = ror(regs[0], size, bits=64)
        elif instList[i+1][0] == 'SHR':
            regs[0] = rol(regs[0], size, bits=64)
        else:
            print("hOI!!")
            exit(1)
    elif ope == 'SHL' or ope == 'SHR' or ope == 'MOVqw' or ope == 'MOVIqw':
        pass
    else:
        print(regs)
        print(ope)
        exit(1)
    #print("R1 = {}".format(hex(regs[0])))

# ECB_1n7e
#for i in range(7):
#    print("R{} = {}".format(i + 1, hex(regs[i])))
print("R1 = {}".format(hex(regs[0])))
