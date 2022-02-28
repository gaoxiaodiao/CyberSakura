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

route = []

def search(field, x, y, move=0):
    global route
    if flag[y][x] != -1 and field[y][x] + 1 > flag[y][x]:
        return False

    field[y][x] += 1

    if compare(field) and move == 36:
        if x == 14 and y == 1:
            print("Found!")
            return True
        else:
            return False

    if move >= 36:
        return False

    if y > 0:
        if x > 0:
            if search(deepcopy(field), x - 1, y - 1, move + 1):
                route.append((-1, -1))
                return True
        else:
            if search(deepcopy(field), x, y - 1, move + 1):
                route.append((-1, -1))
                return True
        if x < 16:
            if search(deepcopy(field), x + 1, y - 1, move + 1):
                route.append((1, -1))
                return True
        else:
            if search(deepcopy(field), x, y - 1, move + 1):
                route.append((1, -1))
                return True
    else:
        if x > 0:
            if search(deepcopy(field), x - 1, y, move + 1):
                route.append((-1, -1))
                return True
        else:
            if search(deepcopy(field), x, y, move + 1):
                route.append((-1, -1))
                return True
        if x < 16:
            if search(deepcopy(field), x + 1, y, move + 1):
                route.append((1, -1))
                return True
        else:
            if search(deepcopy(field), x, y, move + 1):
                route.append((1, -1))
                return True

    if y < 8:
        if x > 0:
            if search(deepcopy(field), x - 1, y + 1, move + 1):
                route.append((-1, 1))
                return True
        else:
            if search(deepcopy(field), x, y + 1, move + 1):
                route.append((-1, 1))
                return True
        if x < 16:
            if search(deepcopy(field), x + 1, y + 1, move + 1):
                route.append((1, 1))
                return True
        else:
            if search(deepcopy(field), x, y + 1, move + 1):
                route.append((1, 1))
                return True
    else:
        if x > 0:
            if search(deepcopy(field), x - 1, y, move + 1):
                route.append((-1, 1))
                return True
        else:
            if search(deepcopy(field), x, y, move + 1):
                route.append((-1, 1))
                return True
        if x < 16:
            if search(deepcopy(field), x + 1, y, move + 1):
                route.append((1, 1))
                return True
        else:
            if search(deepcopy(field), x, y, move + 1):
                route.append((1, 1))
                return True

    return False

field = [[0 for j in range(17)] for i in range(9)]
search(field, 0x50 % 0x12, 0x50 // 0x12)
print(route)
