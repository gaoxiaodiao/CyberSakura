import re
import sys
from ptrlib import *
import itertools
import copy

with open(sys.argv[1], "r") as f:
    instList = []
    for line in f:
        r = re.findall("[0-9a-f]{2}\t(.+) (R\d), (.+)", line)
        if r:
            instList.append(r[0])

def search(instList, current_i, regs, chain=[]):
    for i in range(current_i, len(instList)):
        inst = instList[i]
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
            elif 'MOVIq' in instList[i+1][0] and instList[i+1][1] == inst[2]:
                x = int(instList[i+1][2], 16)
                if regs[0] & x != x:
                    return
                # for ayaC_4.txt
                posList = []
                for l in range(64):
                    if (x >> l) & 1 == 1:
                        posList.append(l)
                for l in range(1, len(posList) + 1):
                    for xorpos in itertools.combinations(posList, l):
                        xx = x
                        for pos in xorpos:
                            xx ^= 1 << pos
                        _regs = copy.deepcopy(regs)
                        #print(hex(regs[0]), hex(regs[0] ^ xx))
                        _regs[0] ^= xx
                        for res in search(instList, i + 1, copy.deepcopy(_regs), chain + [xx]):
                            if res is not None:
                                yield res
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
        #print(ope, print(hex(regs[0])))
    yield regs[0]

        
regs = [0 for i in range(7)]
regs[0] = int(instList[0][2], 16)
for r1 in search(instList, 0, regs):
    try:
        flag = bytes.fromhex(hex(r1)[2:])
    except:
        continue
    for c in flag:
        if not (0x30 <= c <= 0x39 or 0x61 <= c <= ord("z") or c == ord('_') or c == 0):
            break
    else:
        print("R1 = {} : {}".format(hex(r1), flag[::-1]))

# ECB_1n7e
#for i in range(7):
#    print("R{} = {}".format(i + 1, hex(regs[i])))
