def patch(offset, byte):
    x = [-1 for i in range(6)]
    def conv_table():
        return [65, 80, 90, 76, 71, 73, 84, 89, 69, 79, 88, 85, 75, 83, 86, 78]

    def gen_code(x):
        return conv_table()[x]
        
    x[1] = (offset >> 4) & 0b1000
    x[2] = (offset >> 4) & 0b0111
    x[3] = (offset >> 12) & 0b0111
    x[3] |= offset & 0b1000
    x[4] = (offset >> 8) & 0b1000
    x[4] |= offset & 0b0111
    x[5] = (offset >> 8) & 0b0111
    x[0] = byte & 0b0111
    x[0] |= (byte >> 4) & 0b1000
    x[1] |= (byte >> 4) & 0b0111
    x[5] |= byte & 0b1000
    code = [gen_code(x[i]) for i in range(6)]
    return ''.join(list(map(chr, code)))

def apply_patch(code):
    x = [-1 for i in range(6)]
    def conv_table():
        return [65, 80, 90, 76, 71, 73, 84, 89, 69, 79, 88, 85, 75, 83, 86, 78]

    def convert(c):
        table = conv_table()
        if c in table:
            return table.index(c)
        else:
            return -1

    for i in range(6):
        x[i] = convert(ord(code[i]))
    offset = ((x[1] & 0b1000) << 4) | ((x[2] & 0b0111) << 4) | ((x[3] & 0b0111) << 12) | (x[3] & 0b1000) | ((x[4] & 0b1000) << 8) | (x[4] & 0b0111) | ((x[5] & 0b0111) << 8)
    byte = (x[0] & 0b0111) | ((x[0] & 0b1000) << 4) | ((x[1] & 0b0111) << 4) | (x[5] & 0b1000)
    return offset, byte

offset = 0x0622
char = 0x20

code = patch(offset, char)
assert (offset, char) == apply_patch(code)
print(code)
