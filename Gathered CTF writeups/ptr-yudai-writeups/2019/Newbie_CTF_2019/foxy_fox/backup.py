from z3 import *

def calc_hash(name, key):
    hashval = 0
    for c in name:
        print(c)
        hashval = ((c | 0x20) + ((hashval >> 8) | ((hashval & 0xff) << 24))) ^ key
    return hashval

flag = [BitVec("flag{:02x}".format(i), 8) for i in range(0x10)]
s = Solver()
s.add(flag[0x3] == 0x5f)
s.add(flag[0x7] == 0x5f)
s.add(flag[0xc] == 0x5f)
s.add(And(0x40 < flag[0], 0x5a >= flag[0]))
s.add(And(0x40 < flag[1], 0x5a >= flag[1]))
s.add(And(0x40 < flag[2], 0x5a >= flag[2]))
s.add(And(0x40 < flag[4], 0x5a >= flag[4]))
s.add(And(0x40 < flag[5], 0x5a >= flag[5]))
s.add(And(0x40 < flag[6], 0x5a >= flag[6]))
s.add(And(0x40 < flag[8], 0x5a >= flag[8]))
s.add(And(0x40 < flag[9], 0x5a >= flag[9]))
s.add(And(0x40 < flag[10], 0x5a >= flag[10]))
s.add(And(0x40 < flag[11], 0x5a >= flag[11]))
s.add(And(0x40 < flag[13], 0x5a >= flag[13]))
s.add(And(0x40 < flag[14], 0x5a >= flag[14]))
s.add(And(0x40 < flag[15], 0x5a >= flag[15]))

#s.add(calc_hash(flag, 0x7c35d9a3) == 0xf92ac34)

answer = ['?' for i in range(0x10)]
r = s.check()
if r == sat:
    m = s.model()
    for d in m.decls():
        answer[int(d.name()[4:], 16)] = chr(m[d].as_long())
    answer = ''.join(answer)
    print("Found!")
    print(answer)
else:
    print(r)
