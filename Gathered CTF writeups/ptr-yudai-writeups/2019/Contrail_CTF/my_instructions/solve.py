from z3 import *

flag = [BitVec('flag{:02X}'.format(i), 32) for i in range(8)]
s = Solver()


s.add(
    And(
        flag[0] ^ 0x646e3468 == 0, # --> reg0
        flag[1] ^ 0x64346d5f == 0, # --> reg1
        flag[2] ^ (0xffffffff ^ 0xde8ca0cc) == 0, # --> reg2
        flag[3] ^ (0x575f4405 ^ 0x646e3468) == 0, # --> reg3
        ((flag[4] & 0x746e6f63) ^ 0x544c4643) | ((flag[4] | 0x746e6f63) ^ 0x7f6f7f7f) == 0, # --> reg4
        (((flag[5] ^ 0xffffffff) & 0x6c696172) ^ 0x08494010) | (((flag[5] ^ 0x21667463) | 0x6c696172) ^ 0x6e7b6577) == 0, # --> reg5
        (flag[6] - 0x3fb1d * 0x3d6) ^ 0x24232221 == 0, # --> reg6
        ((flag[7] ^ 1436201299) - 75995316) ^ 0x7818f5b8 == 0
    )
)

while True:
    r = s.check()
    if r == sat:
        m = s.model()
        answer = [b'????' for i in range(8)]
        for d in m.decls():
            answer[int(d.name()[4:], 16)] = bytes.fromhex(hex(m[d].as_long())[2:])[::-1]
        print(b''.join(answer))
        s.add(Not(And([flag[int(d.name()[4:], 16)] == m[d] for d in m.decls()])))
    else:
        print(r)
        break
