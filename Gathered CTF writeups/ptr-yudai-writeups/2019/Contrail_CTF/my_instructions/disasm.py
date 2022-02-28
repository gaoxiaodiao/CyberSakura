import struct

def disasm(code):
    def n2r(n): return 'reg{}'.format(n)
    def u32(n): return hex(struct.unpack('<I', n)[0])
    output = []
    pc = 0
    sf, zf = 0, 0
    while len(code) > pc:
        ope = code[pc]
        if ope == 0x10: # mov regX, regY
            output.append('0x{:03X}    mov {}, {}'.format(pc, n2r(code[pc+1]), n2r(code[pc+2])))
            pc += 3
        elif ope == 0x11: # mov regX, IMM
            output.append('0x{:03X}    mov {}, {}'.format(pc, n2r(code[pc+1]), u32(code[pc+2:pc+6])))
            pc += 6
        elif ope == 0x20: # and regX, regY
            output.append('0x{:03X}    and {}, {}'.format(pc, n2r(code[pc+1]), n2r(code[pc+2])))
            pc += 3
        elif ope == 0x21: # and regX, IMM
            output.append('0x{:03X}    and {}, {}'.format(pc, n2r(code[pc+1]), u32(code[pc+2:pc+6])))
            pc += 6
        elif ope == 0x22: # or regX, regY
            output.append('0x{:03X}    or {}, {}'.format(pc, n2r(code[pc+1]), n2r(code[pc+2])))
            pc += 3
        elif ope == 0x23: # or regX, IMM
            output.append('0x{:03X}    or {}, {}'.format(pc, n2r(code[pc+1]), u32(code[pc+2:pc+6])))
            pc += 6
        elif ope == 0x24: # xor regX, regY
            output.append('0x{:03X}    xor {}, {}'.format(pc, n2r(code[pc+1]), n2r(code[pc+2])))
            pc += 3
        elif ope == 0x25: # xor regX, IMM
            output.append('0x{:03X}    xor {}, {}'.format(pc, n2r(code[pc+1]), u32(code[pc+2:pc+6])))
            pc += 6
        elif ope == 0x30: # not regX
            output.append('0x{:03X}    not {}'.format(pc, n2r(code[pc+1])))
            pc += 2
        elif ope == 0x50: # add regX, regY
            output.append('0x{:03X}    add {}, {}'.format(pc, n2r(code[pc+1]), n2r(code[pc+2])))
            pc += 3
        elif ope == 0x51: # add regX, IMM
            output.append('0x{:03X}    add {}, {}'.format(pc, n2r(code[pc+1]), u32(code[pc+2:pc+6])))
            pc += 6
        elif ope == 0x52: # sub regX, regY
            output.append('0x{:03X}    sub {}, {}'.format(pc, n2r(code[pc+1]), n2r(code[pc+2])))
            pc += 3
        elif ope == 0x53: # sub regX, IMM
            output.append('0x{:03X}    sub {}, {}'.format(pc, n2r(code[pc+1]), u32(code[pc+2:pc+6])))
            pc += 6
        elif ope == 0x60: # cmp regX, regY
            output.append('0x{:03X}    cmp {}, {}'.format(pc, n2r(code[pc+1]), n2r(code[pc+2])))
            pc += 3
        elif ope == 0x61: # cmp regX, IMM
            output.append('0x{:03X}    cmp {}, {}'.format(pc, n2r(code[pc+1]), u32(code[pc+2:pc+6])))
            pc += 6
        elif ope == 0x40: # jmp regX
            output.append('0x{:03X}    jmp {}'.format(pc, n2r(code[pc+1])))
            pc += 2
        elif ope == 0x41: # jmp IMM
            output.append('0x{:03X}    jmp {}'.format(pc, u32(code[pc+1:pc+5])))
            pc += 5
        elif ope == 0x42: # jge regX
            output.append('0x{:03X}    jge {}'.format(pc, n2r(code[pc+1])))
            pc += 2
        elif ope == 0x43: # jge IMM
            output.append('0x{:03X}    jge {}'.format(pc, u32(code[pc+1:pc+5])))
            pc += 5
        elif ope == 0x44: # js regX
            output.append('0x{:03X}    js {}'.format(pc, n2r(code[pc+1])))
            pc += 2
        elif ope == 0x45: # js IMM
            output.append('0x{:03X}    js {}'.format(pc, u32(code[pc+1:pc+5])))
            pc += 5
        elif ope == 0x46: # jz regX
            output.append('0x{:03X}    jz {}'.format(pc, n2r(code[pc+1])))
            pc += 2
        elif ope == 0x47: # jz IMM
            output.append('0x{:03X}    jz {}'.format(pc, u32(code[pc+1:pc+5])))
            pc += 5
        elif ope == 0x48: # jnz regX
            output.append('0x{:03X}    jnz {}'.format(pc, n2r(code[pc+1])))
            pc += 2
        elif ope == 0x49: # jnz IMM
            output.append('0x{:03X}    jnz {}'.format(pc, u32(code[pc+1:pc+5])))
            pc += 5
        elif ope == 0xff: # hlt
            output.append('0x{:03X}    assert reg0 == 0'.format(pc))
            pc += 1
        else:
            print("EOA")
            break
    return output

if __name__ == '__main__':
    with open("my_instructions", "rb") as f:
        f.seek(0x3c00)
        code = f.read(0x160)
    print('\n'.join(disasm(code)))
    
