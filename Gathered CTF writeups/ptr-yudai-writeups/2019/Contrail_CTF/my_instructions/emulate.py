reg7 = 0
orig_reg7 = reg7
reg8 = 0x33766f31
reg9 = reg8
reg10 = 0
while reg8 >> 31 == 0:
    reg7 ^= reg8
    reg8 = (reg8 + reg9) & 0xffffffff
print(reg7 ^ orig_reg7)
reg8 = 0x64
reg9 = 0
reg10 = 1
reg11 = 3
reg12 = 5
reg13 = 7
orig_reg7 = reg7
while reg8 >= reg9:
    reg11 -= 1
    reg12 -= 1
    reg13 -= 1
    if reg11 == reg9:
        reg11 = 3
        reg7 = (reg7 + 0x123456) & 0xffffffff
    if reg12 == reg9:
        reg12 = 5
        reg7 = (reg7 + (0xffffffff ^ 0x112233) + 1) & 0xffffffff
    if reg13 == reg9:
        reg13 = 7
        reg7 = (reg7 + (0xffffffff ^ 0x654321) + 1) & 0xffffffff
    reg8 -= reg10
print(reg7 - orig_reg7)
if reg7 ^ 0x7818f5b8 == 0:
    # OK
    pass
