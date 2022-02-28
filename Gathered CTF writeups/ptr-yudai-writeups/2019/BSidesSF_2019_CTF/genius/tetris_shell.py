ofs = 0x15
string = "sh;\xff"

game_object = [0 for i in range(0x1a)]
for i in range(len(string)):
    game_object[ofs + i] = ord(string[i])

bits = ''.join(list(map(lambda x:bin(x)[2:].zfill(8)[::-1], game_object)))
bits += '11'

result = "+" + " " * 10 + "+\n"
for i in range(0, len(bits), 10):
    result += "|"
    for c in bits[i:i+10]:
        result += "." if c == '0' else '#'
    result += "|\n"
result += "+" + "-" * 10 + "+"

print(result)
