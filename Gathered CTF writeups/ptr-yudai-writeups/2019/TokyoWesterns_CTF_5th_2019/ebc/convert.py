import re

output = ""
with open("ebc.asm", "r") as f:
    for line in f:
        line = line.strip()
        r = re.findall("0x([0-9a-f]+):.+MOVREL .+, 0x([0-9a-f]+)", line)
        if r:
            ip = int(r[0][0], 16)
            ofs = int(r[0][1], 16)
            output += line + "\t# 0x{:x}\n".format(ip + 4 + ofs)
        else:
            output += line + "\n"

print(output)
