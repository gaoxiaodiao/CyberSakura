def disasm(code):
    output = []
    pc = 0
    굿 = 0
    jumplist = []
    while True:
        try:
            opecode = code[pc][0].lower()
        except:
            break
        arg = code[pc][1:]
        if opecode == '듃':
            output.append("halt")
        elif opecode == '뉃':
            output.append("reg{} = reg{} + reg{}".format(arg[0], arg[1], arg[2]))
        elif opecode == '렀':
            output.append("reg{} = reg{} ^ reg{}".format(arg[0], arg[1], arg[2]))
        elif opecode == '렳':
            output.append("reg{} = reg{} - reg{}".format(arg[0], arg[1], arg[2]))
        elif opecode == '냃':
            output.append("reg{} = reg{} * reg{}".format(arg[0], arg[1], arg[2]))
        elif opecode == '뢯':
            output.append("reg{} = reg{} / reg{}".format(arg[0], arg[1], arg[2]))
        elif opecode == '륇':
            output.append("reg{} = reg{} & reg{}".format(arg[0], arg[1], arg[2]))
        elif opecode == '맳':
            output.append("reg{} = reg{} | reg{}".format(arg[0], arg[1], arg[2]))
        elif opecode == '괡':
            output.append("nop")
        elif opecode == '뫇':
            output.append("reg{} = reg{}".format(arg[0], arg[1]))
        elif opecode == '꼖':
            if isinstance(arg[1], int):
                output.append("reg{} = {}".format(arg[0], arg[1]))
            else:
                output.append("reg{} = '{}'".format(arg[0], arg[1]))
        elif opecode == '뫻':
            output.append("*({}) = reg{}".format(arg[0], arg[1]))
        elif opecode == '딓':
            output.append("reg{} = *({})".format(arg[0], arg[1]))
        elif opecode == '댒':
            output.append("reg{} = 0".format(arg[0]))
        elif opecode == '묇':
            output.append("*({}) = 0".format(arg[0]))
        elif opecode == '묟':
            output.append("reg{} = input(reg{})".format(arg[0], arg[1]))
        elif opecode == '꽺':
            output.append("*({}) = input(reg{})".format(arg[0], arg[1]))
        elif opecode == '돯':
            output.append("print(reg{})".format(arg[0]))
        elif opecode == '뭗':
            output.append("print(*({}))".format(arg[0]))
        elif opecode == '뭿':
            output.append("goto reg{}".format(arg[0]))
        elif opecode == '뮓':
            output.append("goto *({})".format(arg[0]))
        elif opecode == '뮳':
            output.append("return")
        elif opecode == '믃':
            output.append("if (reg{} > reg{}) call {}".format(arg[1], arg[2], arg[0]))
            # jumplist
        elif opecode == '꽲':
            output.append("if (reg{} != reg{}) call reg{}".format(arg[0], arg[1], arg[2]))
            # jumplist
        elif opecode == '꾮':
            output.append("reg{} = strxor(reg{}, reg{})".format(arg[0], arg[0], arg[1]))
        elif opecode == '꿚':
            output.append("reg{} = strsub(reg{}, reg{})".format(arg[0], arg[0], arg[1]))
        elif opecode == '떇':
            output.append("if (reg{} > reg{}) call reg{}".format(arg[1], arg[2], arg[0]))
            # jumplist
        elif opecode == '뗋':
            output.append("if (reg{} > reg{}) call *({})".format(arg[1], arg[2], arg[0]))
            # jumplist
        elif opecode == '똷':
            output.append("if (reg{} == reg{}) call {}".format(arg[1], arg[2], arg[0]))
            # jumplist
        elif opecode == '뚫':
            output.append("if (reg{} == reg{}) call reg{}".format(arg[1], arg[2], arg[0]))
            # jumplist
        elif opecode == '띇':
            output.append("if (reg{} == reg{}) call *({})".format(arg[1], arg[2], arg[0]))
        else:
            output.append("<ERROR: {}>".format(opecode))
        pc += 1
    return output

code = [
    ['꼖', 0, 'Authentication token: '],
    ['꽺', 0, 0],
    ['꼖', 6, '\xc3\xa1\xc3\x97\xc3\xa4\xc3\x93\xc3\xa2\xc3\xa6\xc3\xad\xc3\xa4\xc3\xa0\xc3\x9f\xc3\xa5\xc3\x89\xc3\x9b\xc3\xa3\xc3\xa5\xc3\xa4\xc3\x89\xc3\x96\xc3\x93\xc3\x89\xc3\xa4\xc3\xa0\xc3\x93\xc3\x89\xc3\x96\xc3\x93\xc3\xa5\xc3\xa4\xc3\x89\xc3\x93\xc3\x9a\xc3\x95\xc3\xa6\xc3\xaf\xc3\xa8\xc3\xa4\xc3\x9f\xc3\x99\xc3\x9a\xc3\x89\xc3\x9b\xc3\x93\xc3\xa4\xc3\xa0\xc3\x99\xc3\x94\xc3\x89\xc3\x93\xc3\xa2\xc3\xa6\xc3\x89\xc3\xa0\xc3\x93\xc3\x9a\xc3\x95\xc3\x93\xc3\x92\xc3\x99\xc3\xa6\xc3\xa4\xc3\xa0\xc3\x89\xc3\xa4\xc3\xa0\xc3\x9f\xc3\xa5\xc3\x89\xc3\x9f\xc3\xa5\xc3\x89\xc3\xa4\xc3\xa0\xc3\x93\xc3\x89\xc3\x9a\xc3\x93\xc3\xa1\xc3\x89\xc2\xb7\xc3\x94\xc3\xa2\xc3\x97\xc3\x9a\xc3\x95\xc3\x93\xc3\x94\xc3\x89\xc2\xb3\xc3\x9a\xc3\x95\xc3\xa6\xc3\xaf\xc3\xa8\xc3\xa4\xc3\x9f\xc3\x99\xc3\x9a\xc3\x89\xc3\x85\xc3\xa4\xc3\x97\xc3\x9a\xc3\x94\xc3\x97\xc3\xa6\xc3\x94\xc3\x89\xc3\x97\xc3\x9a\xc3\xaf\xc3\xa1\xc3\x97\xc3\xaf\xc3\xa5\xc3\x89\xc3\x9f\xc3\x89\xc3\x94\xc3\x99\xc3\x9a\xc3\xa4\xc3\x89\xc3\xa6\xc3\x93\xc3\x97\xc3\x9c\xc3\x9c\xc3\xaf\xc3\x89\xc3\xa0\xc3\x97\xc3\xa2\xc3\x93\xc3\x89\xc3\x97\xc3\x89\xc3\x91\xc3\x99\xc3\x99\xc3\x94\xc3\x89\xc3\xa2\xc3\x9f\xc3\x94\xc3\x89\xc3\x96\xc3\xa3\xc3\xa4\xc3\x89\xc3\x9f\xc3\x89\xc3\xa6\xc3\x93\xc3\x97\xc3\x9c\xc3\x9c\xc3\xaf\xc3\x89\xc3\x93\xc3\x9a\xc3\x9e\xc3\x99\xc3\xaf\xc3\x89\xc3\xa4\xc3\xa0\xc3\x9f\xc3\xa5\xc3\x89\xc3\xa5\xc3\x99\xc3\x9a\xc3\x91\xc3\x89\xc3\x9f\xc3\x89\xc3\xa0\xc3\x99\xc3\xa8\xc3\x93\xc3\x89\xc3\xaf\xc3\x99\xc3\xa3\xc3\x89\xc3\xa1\xc3\x9f\xc3\x9c\xc3\x9c\xc3\x89\xc3\x93\xc3\x9a\xc3\x9e\xc3\x99\xc3\xaf\xc3\x89\xc3\x9f\xc3\xa4\xc3\x89\xc3\x97\xc3\xa5\xc3\xa1\xc3\x93\xc3\x9c\xc3\x9c\xc2\x97\xc3\x89\xc3\xaf\xc3\x99\xc3\xa3\xc3\xa4\xc3\xa3\xc3\x96\xc3\x93\xc2\x9a\xc3\x95\xc3\x99\xc3\x9b\xc2\x99\xc3\xa1\xc3\x97\xc3\xa4\xc3\x95\xc3\xa0\xc2\xa9\xc3\xa2\xc2\xab\xc2\xb3\xc2\xa3\xc3\xaf\xc2\xb2\xc3\x95\xc3\x94\xc3\x88\xc2\xb7\xc2\xb1\xc3\xa2\xc2\xa8\xc3\xab'],
    ['꼖', 2, 2 ** (3 * 2 + 1) - 2 ** (2 + 1)],
    ['꼖', 4, 15],
    ['꼖', 3, 1],
    ['냃', 2, 2, 3],
    ['뉃', 2, 2, 4],
    ['괡', 0, 2],
    ['댒', 3],
    ['꾮', 6, 3],
    ['꼖', 0, 'Thanks.'],
    ['꼖', 1, 'Authorizing access...'],
    ['돯', 0],
    ['딓', 0, 0],
    ['꾮', 0, 2],
    ['꿚', 0, 4],
    ['꼖', 5, 19],
    ['꽲', 0, 6, 5],
    ['돯', 1],
    ['듃'],
    ['꼖', 1, 'Access denied!'],
    ['돯', 1],
    ['듃']
]

for i, inst in enumerate(disasm(code)):
    print("{:08}: {}".format(i, inst))
