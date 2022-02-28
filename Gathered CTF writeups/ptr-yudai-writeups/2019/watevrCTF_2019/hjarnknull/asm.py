import re

def assemble(instructions):
    output = []
    for instr in instructions:
        s = instr.split()
        if s == []: continue
        ope = s[0]
        args = []
        r = re.findall("data\[(\d+)\]", ''.join(s[1:]))
        if r: args += r
        r = re.findall("code\[(\d+)\]", ''.join(s[1:]))
        if r: args += r
        if ope == 'or':
            output.append("eller {} {}".format(args[0], args[1]))
        elif ope == 'not':
            output.append("inte {}".format(args[0]))
        elif ope == 'iseq':
            output.append("testa {} {} {}".format(args[0], args[1], args[2]))
        elif ope == 'ret':
            output.append("poppa")
        elif ope == 'recv':
            output.append("in {}".format(args[0]))
        elif ope == 'chall':
            output.append("ut {}".format(args[0]))
        elif ope == 'shr':
            output.append("hsh {} {}".format(args[0], args[1]))
        elif ope == 'shl':
            output.append("vsh {} {}".format(args[0], args[1]))
        else:
            print("[!] Unknown instruction: `{}`".format(ope))
    output.append("slut 0")
    return output
            
if __name__ == '__main__':
    assemble([
        "or data[0], data[1]",
        "not data[123]",
        "je data[0], data[1] call data[2]",
        "ret",
        "recv data[20]",
        "chall data[20]",
        "shr data[0], data[1]",
        "shl data[3], data[2]",
    ])
