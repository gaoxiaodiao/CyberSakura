from subprocess import check_output
from glob import glob
import re

for filepath in glob("/home/ptr/warehouse/libc-database/db/*.so"):
    result = check_output(["main_arena", filepath])
    r = re.findall(b"0x([0-9a-f]+)", result)
    if not r:
        continue
    if (0x7f4c5cf21b20 - int(r[0], 16)) & 0xfff == 0:
        print(filepath)
