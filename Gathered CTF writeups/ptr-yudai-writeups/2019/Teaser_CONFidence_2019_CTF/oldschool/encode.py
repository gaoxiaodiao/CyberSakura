route = [(1, -1), (1, 1), (1, -1), (-1, 1), (-1, 1), (1, -1), (1, -1), (1, 1), (-1, -1), (1, 1), (1, -1), (-1, 1), (1, -1), (-1, 1), (-1, 1), (-1, -1), (1, -1), (1, 1), (-1, -1), (1, -1), (1, -1), (1, 1), (1, -1), (-1, 1), (-1, 1), (-1, 1), (-1, -1), (1, -1), (1, -1), (1, 1), (-1, -1), (1, 1), (1, -1), (1, -1), (-1, -1), (-1, -1)]
route.reverse()

field = [[0 for j in range(18)] for i in range(9)]
x, y = 0x50 % 0x12, 0x50 // 0x12
for move in route:
    dl = 0
    field[y][x] += 1
    if move[0] == -1:
        if x != 0:
            x -= 1
    else:
        if x != 16:
            x += 1
    if move[1] == -1:
        if y > 0:
            y -= 1
    else:
        if y < 8:
            y += 1
    print(field)

label = " p4{krule_ctf}"
result = ""
for line in field:
    for c in line:
        result += label[c]
    result += "\n"

print(result)
