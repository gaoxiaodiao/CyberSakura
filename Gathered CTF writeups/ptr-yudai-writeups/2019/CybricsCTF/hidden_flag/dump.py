#0xfffff8005daf0000  4d 5a 90 00 03 00 00 00 04 00 00 00 ff ff 00 00   MZ..............

import re

output = b""
with open("flagostor.db", "r") as f:
    for line in f:
        r = re.findall(" ([0-9a-f]{2})", line)
        for i in range(16):
            output += bytes([int(r[i], 16)])
with open("Flagostor.sys", "wb") as f:
    f.write(output)
