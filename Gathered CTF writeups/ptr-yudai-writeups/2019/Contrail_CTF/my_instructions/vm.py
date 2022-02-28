from ptrlib import *

def execute(code, regs):
    pc = 0
    sf, zf = 0, 0
    while True:
        ope = code[pc]
        if ope == 0x10: # mov regX, regY
            regs[code[pc+1]] = regs[code[pc+2]]
            pc += 3
        elif ope == 0x11: # mov regX, IMM
            regs[code[pc+1]] = u32(code[pc+2:pc+6])
            pc += 6
        elif ope == 0x20: # and regX, regY
            regs[code[pc+1]] &= regs[code[pc+2]]
            pc += 3
        elif ope == 0x21: # and regX, IMM
            regs[code[pc+1]] &= u32(code[pc+2:pc+6])
            pc += 6
        elif ope == 0x22: # or regX, regY
            regs[code[pc+1]] |= regs[code[pc+2]]
            pc += 3
        elif ope == 0x23: # or regX, IMM
            regs[code[pc+1]] |= u32(code[pc+2:pc+6])
            pc += 6
        elif ope == 0x24: # xor regX, regY
            regs[code[pc+1]] ^= regs[code[pc+2]]
            pc += 3
        elif ope == 0x25: # xor regX, IMM
            regs[code[pc+1]] ^= u32(code[pc+2:pc+6])
            pc += 6
        elif ope == 0x30: # not regX
            regs[code[pc+1]] = 0xffffffff ^ regs[code[pc+1]]
            pc += 2
        elif ope == 0x50: # add regX, regY
            regs[code[pc+1]] += regs[code[pc+2]]
            pc += 3
        elif ope == 0x51: # add regX, IMM
            regs[code[pc+1]] += u32(code[pc+2:pc+6])
            pc += 6
        elif ope == 0x52: # sub regX, regY
            regs[code[pc+1]] -= regs[code[pc+2]]
            pc += 3
        elif ope == 0x53: # sub regX, IMM
            regs[code[pc+1]] -= u32(code[pc+2:pc+6])
            pc += 6
        elif ope == 0x60: # cmp regX, regY
            delta = regs[code[pc+1]] - regs[code[pc+2]]
            if delta < 0:
                sf = 1
            else:
                zf = 1 if delta == 0 else 0
            pc += 3
        elif ope == 0x61: # cmp regX, IMM
            delta = regs[code[pc+1]] - u32(code[pc+2:pc+6])
            if delta < 0:
                sf = 1
            else:
                zf = 1 if delta == 0 else 0
            pc += 6
        elif ope == 0x40: # jmp regX
            pc = regs[code[pc+1]]
        elif ope == 0x41: # jmp IMM
            pc = u32(code[pc+1:pc+5])
        elif ope == 0x42: # jge regX
            if sf == 0 and zf == 1:
                pc = regs[code[pc+1]]
            else:
                pc += 2
        elif ope == 0x43: # jge IMM
            if sf == 0 and zf == 1:
                pc = u32([code[pc+1:pc+5]])
            else:
                pc += 5
        elif ope == 0x44: # js regX
            if sf:
                pc = regs[code[pc+1]]
            else:
                pc += 2
        elif ope == 0x45: # js IMM
            if sf:
                pc = u32(code[pc+1:pc+5])
            else:
                pc += 5
        elif ope == 0x46: # jz regX
            if zf:
                pc = regs[code[pc+1]]
            else:
                pc += 2
        elif ope == 0x47: # jz IMM
            if zf:
                pc = u32(code[pc+1:pc+5])
            else:
                pc += 5
        elif ope == 0x48: # jnz regX
            if zf:
                pc += 2
            else:
                pc = regs[code[pc+1]]
        elif ope == 0x49: # jnz IMM
            if zf:
                pc += 5
            else:
                pc = u32(code[pc+1:pc+5])
        elif ope == 0xff: # hlt
            return

if __name__ == '__main__':
    code = b''
    code += bytes([])
    regs = list(code)
    execute(code, regs)
