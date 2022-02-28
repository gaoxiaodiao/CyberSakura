import struct
#"""
mem = [0x42, 0x00, 0x01, 0x00, 0x00, 0x00, 0x42, 0x01, 0x01, 0x00, 
  0x00, 0x00, 0x42, 0x02, 0x00, 0x00, 0x00, 0x00, 0x48, 0x02, 
  0x64, 0x00, 0x00, 0x00, 0x92, 0x30, 0x00, 0x00, 0x00, 0x02, 
  0x03, 0x01, 0x03, 0x03, 0x00, 0x02, 0x00, 0x01, 0x02, 0x01, 
  0x03, 0x13, 0x02, 0x90, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00]
"""
mem = []
mem += [10, 0, 0xde, 0xad, 0xbe, 0xef]
mem += [11, 0, 11, 12, 13, 14]
#"""

eip = 0

def p32():
    global mem, eip
    eip += 4
    l = ''.join(map(chr, mem[eip-4:eip]))
    return struct.unpack("<I", l)[0]

def disas():
    ans = []
    global mem, eip
    targets = [eip]
    visited = {}
    while targets:
        eip = targets.pop(0)
        if eip in visited:
            continue
        visited[eip] = 1
        try:
            eip -= 1
            while eip < len(mem):
                eip += 1
                b = mem[eip]
                op, hi = b & 0x3f, b >> 6
                if op == 0:
                    ans.append([eip, "ret"])
                elif op == 1:
                    ans.append([eip, "nop"])
                elif op == 2:
                    eip += 1
                    a = mem[eip] & 0xf
                    eip += 1
                    if hi == 0:
                        b = mem[eip] & 0xf
                        ans.append([eip-2, "mov r%d, r%d", a, b])
                    else:
                        w = p32()
                        ans.append([eip-6, "mov r%d, %#x", a, w])
                        eip -= 1
                elif op == 3:
                    eip += 1
                    a = mem[eip] & 0xf
                    eip += 1
                    if hi == 0:
                        b = mem[eip] & 0xf
                        ans.append([eip-2, "add r%d, r%d", a, b])
                    else:
                        w = p32()
                        ans.append([eip-6, "add r%d, %#x", a, w])
                        eip -= 1
                elif op == 4:
                    eip += 1
                    a = mem[eip] & 0xf
                    eip += 1
                    if hi == 0:
                        b = mem[eip] & 0xf
                        ans.append([eip-2, "sub r%d, r%d", a, b])
                    else:
                        w = p32()
                        ans.append([eip-6, "sub r%d, %#x", a, w])
                        eip -= 1
                elif op == 5:
                    eip += 1
                    a = mem[eip] & 0xf
                    eip += 1
                    if hi == 0:
                        b = mem[eip] & 0xf
                        ans.append([eip-2, "and r%d, r%d", a, b])
                    else:
                        w = p32()
                        ans.append([eip-6, "and r%d, %#x", a, w])
                        eip -= 1
                elif op == 6:
                    eip += 1
                    a = mem[eip] & 0xf
                    eip += 1
                    if hi == 0:
                        b = mem[eip] & 0xf
                        ans.append([eip-2, "or r%d, r%d", a, b])
                    else:
                        w = p32()
                        ans.append([eip-6, "or r%d, %#x", a, w])
                        eip -= 1
                elif op == 7:
                    eip += 1
                    a = mem[eip] & 0xf
                    eip += 1
                    if hi == 0:
                        b = mem[eip] & 0xf
                        ans.append([eip-2, "xor r%d, r%d", a, b])
                    else:
                        w = p32()
                        ans.append([eip-6, "xor r%d, %#x", a, w])
                        eip -= 1
                elif op == 8:
                    if hi == 0:
                        eip += 1
                        a = mem[eip] & 0xf
                        eip += 1
                        b = mem[eip] & 0xf
                        ans.append([eip-2, "cmp r%d, r%d", a, b])
                    elif hi == 1:
                        eip += 1
                        a = mem[eip] & 0xf
                        eip += 1
                        imm = p32()
                        ans.append([eip-6, "cmp r%d, %#x", a, imm])
                        eip -= 1
                    else:
                        eip += 1
                        imm_a = p32()
                        imm_b = p32()
                        ans.append([eip-8, "cmp %#x, %#x", imm_a, imm_b])
                        eip -= 1
                elif op == 9:
                    if hi == 0:
                        eip += 1
                        a = mem[eip] & 0xf
                        eip += 1
                        b = mem[eip] & 0xf
                        ans.append([eip-2, "test r%d, r%d", a, b])
                    elif hi == 1:
                        eip += 1
                        a = mem[eip] & 0xf
                        eip += 1
                        imm = p32()
                        ans.append([eip-6, "test r%d, %#x", a, imm])
                        eip -= 1
                    else:
                        eip += 1
                        imm_a = p32()
                        imm_b = p32()
                        ans.append([eip-8, "test %#x, %#x", imm_a, imm_b])
                        eip -= 1
                elif op == 10:
                    eip += 1
                    a = mem[eip] & 0xf
                    eip += 1
                    imm = p32()
                    ans.append([eip-6, "mov r%d, [%#x]", a, imm])
                    eip -= 1
                elif op == 11:
                    eip += 1
                    a = mem[eip] & 0xf
                    eip += 1
                    imm = p32()
                    ans.append([eip-6, "mov [%#x], r%d", imm, a])
                    eip -= 1
                elif op == 12:
                    eip += 1
                    if hi == 0:
                        a = mem[eip] & 0xf
                        ans.append([eip-1, "call r%d", a])
                        eip -= 1
                    else:
                        imm = p32()
                        ans.append([eip-5, "call %#x", imm])
                        targets.append(imm)
                        eip -= 1
                elif op == 13:
                    # if stack is empty, return to last eip
                    ans.append([eip, "chk.ret"])
                elif op == 14:
                    # if stack is empty, return to last eip
                    eip += 1
                    if hi == 0:
                        a = mem[eip] & 0xf
                        ans.append([eip-1, "push r%d", a])
                    else:
                        imm = p32()
                        ans.append([eip-5, "push %#x", imm])
                        eip -= 1
                elif op == 15:
                    # if stack is empty, return to last eip
                    eip += 1
                    a = mem[eip] & 0xf
                    ans.append([eip-1, "pop r%d", a])
                elif op == 16:
                    eip += 1
                    if hi == 0:
                        a = mem[eip] & 0xf
                        ans.append([eip-1, "jmp r%d", a])
                    else:
                        imm = p32()
                        ans.append([eip-5, "jmp %#x", imm])
                        targets.append(imm)
                        eip -= 1
                elif op == 17:
                    eip += 1
                    if hi == 0:
                        a = mem[eip] & 0xf
                        ans.append([eip-1, "jz r%d", a])
                    else:
                        imm = p32()
                        ans.append([eip-5, "jz %#x", imm])
                        eip -= 1
                elif op == 18:
                    eip += 1
                    if hi == 0:
                        a = mem[eip] & 0xf
                        ans.append([eip-1, "jle r%d", a])
                    else:
                        imm = p32()
                        ans.append([eip-5, "jle %#x", imm])
                        targets.append(imm)
                        eip -= 1
                elif op == 19:
                    eip += 1
                    a = mem[eip] & 0xf
                    ans.append([eip-1, "inc r%d", a])
                elif op == 20:
                    eip += 1
                    a = mem[eip] & 0xf
                    ans.append([eip-1, "dec r%d", a])
                else:
                    """ return 5 """
                    pass
        except Exception, e:
            print(e)
    ans.sort(key=lambda i: i[0])
    visited = {}
    for i in ans:
        if i[0] in visited:
            continue
        visited[i[0]] = 1
        print "%02x" % i[0], "\t",
        print i[1] % tuple(i[2:])

print(disas())
