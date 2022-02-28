from z3 import *

flag = [BitVec("flag{:02x}".format(i), 8) for i in range(0x27)]
s = Solver()
s.add(flag[0] == ord("T"))
s.add(flag[1] == ord("W"))
s.add(flag[2] == ord("C"))
s.add(flag[3] == ord("T"))
s.add(flag[4] == ord("F"))
s.add(flag[5] == ord("{"))
s.add(flag[0x26] == ord("}"))
s.add(flag[0x25] == ord("5"))
s.add(flag[0x07] == ord("f"))
s.add(flag[0x0B] == ord("8"))
s.add(flag[0x0C] == ord("7"))
s.add(flag[0x17] == ord("2"))
s.add(flag[0x1F] == ord("4"))

for i in range(8):
    su = 0
    xo = 0
    for j in range(4):
        su += flag[6 + i * 4 + j]
        xo ^= flag[6 + i * 4 + j]
    s.add(su == [0x15e, 0xda, 0x12f, 0x131, 0x100, 0x131, 0xfb, 0x102][i])
    s.add(xo == [0x52, 0x0c, 0x01, 0x0f, 0x5c, 0x05, 0x53, 0x58][i])

for i in range(8):
    su = 0
    xo = 0
    for j in range(4):
        su += flag[6 + i + j * 8]
        xo ^= flag[6 + i + j * 8]
    s.add(su == [0x129, 0x103, 0x12b, 0x131, 0x135, 0x10b, 0xff, 0xff][i])
    s.add(xo == [0x01, 0x57, 0x07, 0x0d, 0x0d, 0x53, 0x51, 0x51][i])

nazoTable = [0x80, 0x80, 0xff, 0x80, 0xff, 0xff, 0xff, 0xff, 0x80, 0xff, 0xff, 0x80, 0x80, 0xff, 0xff, 0x80, 0xff, 0xff, 0x80, 0xff, 0x80, 0x80, 0xff, 0xff, 0xff, 0xff, 0x80, 0xff, 0xff, 0xff, 0x80, 0xff]
for i in range(0x20):
    s.add(flag[6 + i] != 0x33)
    if nazoTable[i] == 0x80:
        s.add(0x61 <= flag[6 + i], flag[6 + i] <= 0x66)
    else:
        s.add(0x30 <= flag[6 + i], flag[6 + i] <= 0x39)

su = 0
for i in range(0x10):
    su += flag[(i + 3) * 2]
s.add(su == 0x488)

while True:
    answer = ['?' for i in range(0x27)]
    r = s.check()
    if r == sat:
        m = s.model()
        for d in m.decls():
            answer[int(d.name()[4:], 16)] = chr(m[d].as_long())
        answer = ''.join(answer)
        for i, c in enumerate("0123456789abcdef"):
            if answer.count(c) != [3, 2, 2, 0, 3, 2, 1, 3, 3, 1, 1, 3, 1, 2, 2, 3][i]: break
        else:
            print("Found!")
            print(answer)
            exit(0)
        s.add(Not(And([flag[int(d.name()[4:], 16)] == m[d] for d in m.decls()])))
        print(answer)
    else:
        print(r)
