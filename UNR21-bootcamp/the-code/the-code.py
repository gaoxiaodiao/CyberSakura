import base64
import sys
import string


def lower(enc_st, i):
    return enc_st[:i] + enc_st[i].lower() + enc_st[i + 1:]


def score(s, posmax):
    score = 0
    alphabet = string.printable[:-2].encode()
    dec = base64.b64decode(s)
    if dec[0] not in alphabet:
        return -1
    while score < (posmax * 6 // 8 + 6) and dec[score] in alphabet:
        score += 1
    return score - 1


def tryToLower(enc_st, pos):
    encs = []
    scores = []
    for i in range(256):
        enc = enc_st
        b = bin(i)[2:]
        if len(b) < 8:
            b = "0" * (8 - len(b)) + b
        for offset, shouldLower in enumerate(b):
            if shouldLower == "1":
                enc = lower(enc, pos + offset)
        encs.append(enc)
        scores.append(score(enc, pos))
    max = -1
    posmax = -1
    for i, s in enumerate(scores):
        if s > max:
            max = s
            posmax = i
    arr = []
    verif = []
    for i, s in enumerate(scores):
        if s == max and encs[i] not in verif:
            verif.append(encs[i])
            arr.append(i)
    if len(arr) == 1:
        return encs[posmax]
    else:
        print("CHOICE TIME")
        for i in arr:
                print(str(i).encode() + b'. ' + base64.b64decode(encs[i]))
        x = input()
        return encs[int(x)]


enc = sys.argv[1]
for i in range(0, len(enc), 8):
    enc = tryToLower(enc, i)
print(base64.b64decode(enc))
