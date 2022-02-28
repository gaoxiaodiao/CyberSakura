from ptrlib import *

encrypted = open("eflag.txt", "rb").read()

flag = ""
p = Process(["gdb", "-q", "./encrypt"])
p.sendlineafter("pwndbg>", "break *0x555555555148")
p.sendlineafter("pwndbg>", "run")
logger.info("Created process")
p.sendlineafter("pwndbg>", "checkpoint")
logger.info("Created checkpoint")

for i in range(len(encrypted)):
    found = False
    for ci in range(0x20, 0x7F):
        c = chr(ci)
        out, err = p.communicate((flag + c).encode())
        if out == encrypted[: i + 1]:
            flag += c
            print(flag)
            found = True
            break
    if not found:
        print("[+]ERR")
        exec()
