pubkey = 569581432115411077780908947843367646738369018797567841

with open("flag.enc") as f:
    encoded = f.read()

flag = ""
for c in encoded.split(','):
    if not c: break
    if int(c, 16) != 0:
        flag += "0"
    else:
        flag += "1"

print(hex(int(flag, 2))[2:].rstrip("L").decode("hex"))
