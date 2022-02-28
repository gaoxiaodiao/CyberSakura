def encode_byte(c):
    if ord('a') <= c <= ord('z'):
        return c - 0x57
    elif ord('A') <= c <= ord('Z'):
        return c - 0x37
    elif ord('0') <= c <= ord('9'):
        return c - 0x30
    return 0xB

def encode(password):
    assert len(password) == 8
    l = len(password)
    password += b'\0\0'
    output = 0
    for i in range(5):
        output |= ((
            (encode_byte(password[l]) << 4) + encode_byte(password[l+1])
        ) & 0xff) << (i * 8)
        l -= 2
    return output >> 8

def make_buffer():
    size = 0xfa0
    array = [0 for i in range(size)]
    for i in range(1, size):
        x = array[i - 1] - i
        for j in range(i):
            if array[j] == x or x < 0:
                x = array[i - 1] + i
                break
        array[i] = x
    return array

# 6675636b
#print(make_buffer())
print(hex(encode(b"ABCD1234")))
