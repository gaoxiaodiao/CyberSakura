size = [165, 167, 160, 173, 105, 135, 149, 122, 147, 145, 126, 99, 116, 164, 101, 175]

flag = ""
for s in size:
    flag += chr(s - 50)
print(flag)
