from copy import deepcopy

flag = [
    [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 3, 2, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 4, 2, 3, 0, -1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 2, 2, 1, 3, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

def compare(field):
    for y in range(9):
        for x in range(17):
            if y == 32 // 0x12 and x == 32 % 0x12:
                continue
            if y == 0x50 // 0x12 and x == 0x50 % 0x12:
                continue
            if flag[y][x] != field[y][x]:
                return False
    return True

def decode(route):
    result = ''
    bit = ''
    i = 0
    for move in route:
        if move[0] == 1:
            bit += '1'
        elif move[0] == -1:
            bit += '0'

        if move[1] == 1:
            bit += '1'
        elif move[1] == -1:
            bit += '0'

        i += 1
        if i == 4:
            result += bit[::-1]
            bit = ''
            i = 0
    return b''.fromhex(hex(int(result, 2))[2:])

def search(field, x, y, route, move=0):
    if flag[y][x] != -1 and field[y][x] + 1 > flag[y][x]:
        return False

    field[y][x] += 1

    if compare(field) and move == 36:
        if x == 14 and y == 1:
            w = decode(route)
            for c in w:
                if ord(" ") < c < ord("~"):
                    continue
                else:
                    break
            else:
                print(w)
            return True
        else:
            return False

    if move == 36:
        return False

    if y > 0:
        if x > 0:
            search(deepcopy(field), x - 1, y - 1, route + [(-1, -1)], move + 1)
        else:
            search(deepcopy(field), x, y - 1, route + [(-1, -1)], move + 1)
        if x < 16:
            search(deepcopy(field), x + 1, y - 1, route + [(1, -1)], move + 1)
        else:
            search(deepcopy(field), x, y - 1, route + [(1, -1)], move + 1)
    else:
        if x > 0:
            search(deepcopy(field), x - 1, y, route + [(-1, -1)], move + 1)
        else:
            search(deepcopy(field), x, y, route + [(-1, -1)], move + 1)
        if x < 16:
            search(deepcopy(field), x + 1, y, route + [(1, -1)], move + 1)
        else:
            search(deepcopy(field), x, y, route + [(1, -1)], move + 1)

    if y < 8:
        if x > 0:
            search(deepcopy(field), x - 1, y + 1, route + [(-1, 1)], move + 1)
        else:
            search(deepcopy(field), x, y + 1, route + [(-1, 1)], move + 1)
        if x < 16:
            search(deepcopy(field), x + 1, y + 1, route + [(1, 1)], move + 1)
        else:
            search(deepcopy(field), x, y + 1, route + [(1, 1)], move + 1)
    else:
        if x > 0:
            search(deepcopy(field), x - 1, y, route + [(-1, 1)], move + 1)
        else:
            search(deepcopy(field), x, y, route + [(-1, 1)], move + 1)
        if x < 16:
            search(deepcopy(field), x + 1, y, route + [(1, 1)], move + 1)
        else:
            search(deepcopy(field), x, y, route + [(1, 1)], move + 1)

    return False

field = [[0 for j in range(17)] for i in range(9)]

# initialize
x, y = 0x50 % 0x12, 0x50 // 0x12
known = "p4{"

route = []
cnt = 0
for c in known:
    dl = ord(c)
    for i in range(4):
        move = [0, 0]
        if dl & 1 == 0:
            move[0] = -1
            if x > 0:
                x -= 1
        else:
            move[0] = 1
            if x < 16:
                x += 1
        if dl & 2 == 0:
            move[1] = -1
            if y > 0:
                y -= 1
        else:
            move[1] = 1
            if y < 8:
                y += 1
        route.append(tuple(move))
        cnt += 1
        dl >>= 2
        field[y][x] += 1
        if flag[y][x] != -1 and field[y][x] > flag[y][x]:
            print("ERROR!")
            exit(1)

print(route)

label = ".p4{krule_ctf}"
result = ""
for line in field:
    for c in line:
        if len(label) > c:
            result += label[c]
        else:
            result += chr(c)
    result += "\n"
print(result)
print(x, y)
field[y][x] -= 1
search(field, x, y, route, cnt)
