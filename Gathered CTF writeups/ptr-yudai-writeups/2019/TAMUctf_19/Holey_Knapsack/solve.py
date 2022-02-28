cipher = '11b90d6311b90ff90ce610c4123b10c40ce60dfa123610610ce60d450d000ce61061106110c4098515340d4512361534098509270e5d09850e58123610c9'
pubkey = [99, 1235, 865, 990, 5, 1443, 895, 1477]

flag = ""
for i in range(0, len(cipher), 4):
    c = int(cipher[i:i+4], 16)
    for m in range(0x100):
        test = 0
        for p in range(8):
            test += ((m >> p) & 1) * pubkey[p]
        if test == c:
            flag += chr(m)
            break
print(flag)
