# Source Generated with Decompyle++
# File: 3nohtyp.pyc (Python 3.6)
def run_vm(instructions):
    pc = 0
    굿 = 0
    regs = [0] * 2 ** (2 * 2)
    mem = [0] * 100
    jmplist = []
    while instructions[pc][0] != '\xeb\x93\x83':
        ope = instructions[pc][0].lower()
        operand = instructions[pc][1:]
        if ope == '\xeb\x89\x83':
            regs[operand[0]] = regs[operand[1]] + regs[operand[2]]
        elif ope == '\xeb\xa0\x80':
            regs[operand[0]] = regs[operand[1]] ^ regs[operand[2]]
        elif ope == '\xeb\xa0\xb3':
            regs[operand[0]] = regs[operand[1]] - regs[operand[2]]
        elif ope == '\xeb\x83\x83':
            regs[operand[0]] = regs[operand[1]] * regs[operand[2]]
        elif ope == '\xeb\xa2\xaf':
            regs[operand[0]] = regs[operand[1]] / regs[operand[2]]
        elif ope == '\xeb\xa5\x87':
            regs[operand[0]] = regs[operand[1]] & regs[operand[2]]
        elif ope == '\xeb\xa7\xb3':
            regs[operand[0]] = regs[operand[1]] | regs[operand[2]]
        elif ope == '\xea\xb4\xa1':
            regs[operand[0]] = regs[operand[0]]
        elif ope == '\xeb\xab\x87':
            regs[operand[0]] = regs[operand[1]]
        elif ope == '\xea\xbc\x96':
            regs[operand[0]] = operand[1]
        elif ope == '\xeb\xab\xbb':
            mem[operand[0]] = regs[operand[1]]
        elif ope == '\xeb\x94\x93':
            regs[operand[0]] = mem[operand[1]]
        elif ope == '\xeb\x8c\x92':
            regs[operand[0]] = 0
        elif ope == '\xeb\xac\x87':
            mem[operand[0]] = 0
        elif ope == '\xeb\xac\x9f':
            regs[operand[0]] = input(regs[operand[1]])
        elif ope == '\xea\xbd\xba':
            mem[operand[0]] = input(regs[operand[1]])
        elif ope == '\xeb\x8f\xaf':
            print(regs[operand[0]])
        elif ope == '\xeb\xad\x97':
            print(mem[operand[0]])
        elif ope == '\xeb\xad\xbf':
            pc = regs[operand[0]]
        elif ope == '\xeb\xae\x93':
            pc = mem[operand[0]]
        elif ope == '\xeb\xae\xb3':
            pc = jmplist.pop()
        elif ope == '\xeb\xaf\x83' and regs[operand[1]] > regs[operand[2]]:
            pc = operand[0]
            jmplist.append(pc)
            continue
        elif ope == '\xea\xbd\xb2':
            regs[7] = 0
            for i in range(len(regs[operand[0]])):
                if regs[operand[0]] != regs[operand[1]]:
                    regs[7] = 1
                    pc = regs[operand[2]]
                    jmplist.append(pc)
        elif ope == '\xea\xbe\xae':
            괢 = ''
            for i in range(len(regs[operand[0]])):
                괢 += chr(ord(regs[operand[0]][i]) ^ regs[operand[1]])
            
            regs[operand[0]] = 괢
        elif ope == '\xea\xbf\x9a':
            괢 = ''
            for i in range(len(regs[operand[0]])):
                괢 += chr(ord(regs[operand[0]][i]) - regs[operand[1]])
            
            regs[operand[0]] = 괢
        elif ope == '\xeb\x96\x87' and regs[operand[1]] > regs[operand[2]]:
            pc = regs[operand[0]]
            jmplist.append(pc)
            continue
        elif ope == '\xeb\x97\x8b' and regs[operand[1]] > regs[operand[2]]:
            pc = mem[operand[0]]
            jmplist.append(pc)
            continue
        elif ope == '\xeb\x98\xb7' and regs[operand[1]] == regs[operand[2]]:
            pc = operand[0]
            jmplist.append(pc)
            continue
        elif ope == '\xeb\x9a\xab' and regs[operand[1]] == regs[operand[2]]:
            pc = regs[operand[0]]
            jmplist.append(pc)
            continue
        elif ope == '\xeb\x9d\x87' and regs[operand[1]] == regs[operand[2]]:
            pc = mem[operand[0]]
            jmplist.append(pc)
            continue
        pc += 1

run_vm([
    [
        '\xea\xbc\x96',
        0,
        'Authentication token: '],
    [
        '\xea\xbd\xba',
        0,
        0],
    [
        '\xea\xbc\x96',
        6,
        '\xc3\xa1\xc3\x97\xc3\xa4\xc3\x93\xc3\xa2\xc3\xa6\xc3\xad\xc3\xa4\xc3\xa0\xc3\x9f\xc3\xa5\xc3\x89\xc3\x9b\xc3\xa3\xc3\xa5\xc3\xa4\xc3\x89\xc3\x96\xc3\x93\xc3\x89\xc3\xa4\xc3\xa0\xc3\x93\xc3\x89\xc3\x96\xc3\x93\xc3\xa5\xc3\xa4\xc3\x89\xc3\x93\xc3\x9a\xc3\x95\xc3\xa6\xc3\xaf\xc3\xa8\xc3\xa4\xc3\x9f\xc3\x99\xc3\x9a\xc3\x89\xc3\x9b\xc3\x93\xc3\xa4\xc3\xa0\xc3\x99\xc3\x94\xc3\x89\xc3\x93\xc3\xa2\xc3\xa6\xc3\x89\xc3\xa0\xc3\x93\xc3\x9a\xc3\x95\xc3\x93\xc3\x92\xc3\x99\xc3\xa6\xc3\xa4\xc3\xa0\xc3\x89\xc3\xa4\xc3\xa0\xc3\x9f\xc3\xa5\xc3\x89\xc3\x9f\xc3\xa5\xc3\x89\xc3\xa4\xc3\xa0\xc3\x93\xc3\x89\xc3\x9a\xc3\x93\xc3\xa1\xc3\x89\xc2\xb7\xc3\x94\xc3\xa2\xc3\x97\xc3\x9a\xc3\x95\xc3\x93\xc3\x94\xc3\x89\xc2\xb3\xc3\x9a\xc3\x95\xc3\xa6\xc3\xaf\xc3\xa8\xc3\xa4\xc3\x9f\xc3\x99\xc3\x9a\xc3\x89\xc3\x85\xc3\xa4\xc3\x97\xc3\x9a\xc3\x94\xc3\x97\xc3\xa6\xc3\x94\xc3\x89\xc3\x97\xc3\x9a\xc3\xaf\xc3\xa1\xc3\x97\xc3\xaf\xc3\xa5\xc3\x89\xc3\x9f\xc3\x89\xc3\x94\xc3\x99\xc3\x9a\xc3\xa4\xc3\x89\xc3\xa6\xc3\x93\xc3\x97\xc3\x9c\xc3\x9c\xc3\xaf\xc3\x89\xc3\xa0\xc3\x97\xc3\xa2\xc3\x93\xc3\x89\xc3\x97\xc3\x89\xc3\x91\xc3\x99\xc3\x99\xc3\x94\xc3\x89\xc3\xa2\xc3\x9f\xc3\x94\xc3\x89\xc3\x96\xc3\xa3\xc3\xa4\xc3\x89\xc3\x9f\xc3\x89\xc3\xa6\xc3\x93\xc3\x97\xc3\x9c\xc3\x9c\xc3\xaf\xc3\x89\xc3\x93\xc3\x9a\xc3\x9e\xc3\x99\xc3\xaf\xc3\x89\xc3\xa4\xc3\xa0\xc3\x9f\xc3\xa5\xc3\x89\xc3\xa5\xc3\x99\xc3\x9a\xc3\x91\xc3\x89\xc3\x9f\xc3\x89\xc3\xa0\xc3\x99\xc3\xa8\xc3\x93\xc3\x89\xc3\xaf\xc3\x99\xc3\xa3\xc3\x89\xc3\xa1\xc3\x9f\xc3\x9c\xc3\x9c\xc3\x89\xc3\x93\xc3\x9a\xc3\x9e\xc3\x99\xc3\xaf\xc3\x89\xc3\x9f\xc3\xa4\xc3\x89\xc3\x97\xc3\xa5\xc3\xa1\xc3\x93\xc3\x9c\xc3\x9c\xc2\x97\xc3\x89\xc3\xaf\xc3\x99\xc3\xa3\xc3\xa4\xc3\xa3\xc3\x96\xc3\x93\xc2\x9a\xc3\x95\xc3\x99\xc3\x9b\xc2\x99\xc3\xa1\xc3\x97\xc3\xa4\xc3\x95\xc3\xa0\xc2\xa9\xc3\xa2\xc2\xab\xc2\xb3\xc2\xa3\xc3\xaf\xc2\xb2\xc3\x95\xc3\x94\xc3\x88\xc2\xb7\xc2\xb1\xc3\xa2\xc2\xa8\xc3\xab'],
    [
        '\xea\xbc\x96',
        2,
        2 ** (3 * 2 + 1) - 2 ** (2 + 1)],
    [
        '\xea\xbc\x96',
        4,
        15],
    [
        '\xea\xbc\x96',
        3,
        1],
    [
        '\xeb\x83\x83',
        2,
        2,
        3],
    [
        '\xeb\x89\x83',
        2,
        2,
        4],
    [
        '\xea\xb4\xa1',
        0,
        2],
    [
        '\xeb\x8c\x92',
        3],
    [
        '\xea\xbe\xae',
        6,
        3],
    [
        '\xea\xbc\x96',
        0,
        'Thanks.'],
    [
        '\xea\xbc\x96',
        1,
        'Authorizing access...'],
    [
        '\xeb\x8f\xaf',
        0],
    [
        '\xeb\x94\x93',
        0,
        0],
    [
        '\xea\xbe\xae',
        0,
        2],
    [
        '\xea\xbf\x9a',
        0,
        4],
    [
        '\xea\xbc\x96',
        5,
        19],
    [
        '\xea\xbd\xb2',
        0,
        6,
        5],
    [
        '\xeb\x8f\xaf',
        1],
    [
        '\xeb\x93\x83'],
    [
        '\xea\xbc\x96',
        1,
        'Access denied!'],
    [
        '\xeb\x8f\xaf',
        1],
    [
        '\xeb\x93\x83']])
