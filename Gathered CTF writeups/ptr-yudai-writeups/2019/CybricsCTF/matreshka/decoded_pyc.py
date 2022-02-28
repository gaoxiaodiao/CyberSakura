
def decode(data, key):
    idx = 0
    res = []
    for c in data:
        res.append(chr(c ^ ord(key[idx])))
        idx = (idx + 1) % len(key)

    return res


flag = [
 40, 11, 82, 58, 93, 82, 64, 76, 6, 70, 100, 26, 7, 4, 123, 124, 127, 45, 1, 125, 107, 115, 0, 2, 31, 15]
print('Enter key to get flag:')
key = input()
if len(key) != 8:
    print('Invalid len')
    quit()
res = decode(flag, key)
print(''.join(res))
