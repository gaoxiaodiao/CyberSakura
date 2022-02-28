with open("flag.txt", "rb") as f:
    cipher = f.read()

flag = ''
for block in cipher.split():
    for c in block.split(b'-'):
        if c == b'di' or c == b'dit':
            flag += '.'
        elif c == b'dah':
            flag += '_'
        else:
            print(c)
            print("Something is wrong......")
            exit(1)
    flag += ' '
print(flag)
