result = ""
table = {
    'kappa_pride': '2',
    'pepe': '3',
    'kappa': '0',
    'look_at_this_dude': '4',
    'trollface': '1'
}
with open("meme_or_not", "r") as f:
    for line in f:
        cs = line.split()
        char = ''
        for c in cs:
            char += table[c]
        result += chr(int(char, 5))
print(result)
