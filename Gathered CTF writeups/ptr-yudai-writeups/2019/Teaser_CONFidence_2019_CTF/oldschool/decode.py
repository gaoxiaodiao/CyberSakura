route = [(1, -1), (1, 1), (1, -1), (-1, 1), (-1, 1), (1, -1), (1, -1), (1, 1), (-1, -1), (1, 1), (1, -1), (-1, 1), (1, -1), (-1, 1), (-1, 1), (-1, -1), (1, -1), (1, 1), (-1, -1), (1, -1), (1, -1), (1, 1), (1, -1), (-1, 1), (-1, 1), (-1, 1), (-1, -1), (1, -1), (1, -1), (1, 1), (-1, -1), (1, 1), (1, -1), (1, -1), (-1, -1), (-1, -1)]
route.reverse()
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

print(result)
print(len(route))