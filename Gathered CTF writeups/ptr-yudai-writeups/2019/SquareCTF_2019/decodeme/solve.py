import string
import base64

with open("decodeme.png.enc", "r") as f:
    buf = f.read()

ofs = -1
pre = 0
output = ''
while b'\x00' in buf[ofs+1:]:
    ofs = buf.index(b'\x00', ofs + 1)
    local = buf[pre:ofs]
    s = local[:len(string.printable)]
    past = []
    #print(repr(buf[pre:ofs + 1]))
    for r in s:
        diff = local.count(r)
        if diff == 0: break
        if r in past: break
        past.append(r)
        r = ord(r)
        if r + diff <= ord('z'):
            if r + diff < 0x20:
                x = r + diff + len(string.printable)
            else:
                x = r + diff
        else:
            x = r + diff - len(string.printable)
        output += chr(x)
    pre = ofs + 1

local = buf[ofs + 1:]
s = local[:len(string.printable)]
past = []
for r in s:
    diff = local.count(r)
    if diff == 0: break
    if r in past: break
    past.append(r)
    r = ord(r)
    if r + diff <= ord('z'):
        if r + diff < 0x20:
            x = r + diff + len(string.printable)
        else:
            x = r + diff
    else:
        x = r + diff - len(string.printable)
    output += chr(x)

print(output)
with open("output.png", "w") as f:
    f.write(base64.b64decode(output))
