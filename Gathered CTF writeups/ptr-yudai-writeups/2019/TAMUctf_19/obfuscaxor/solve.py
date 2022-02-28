from ptrlib import *
import re
import string

offset = 8
key = ["A" for i in range(16)]
# known: 'p3Asujmn'
key[0] = 'p'
key[1] = '3'
key[2] = 'A'
key[3] = 's'
key[4] = 'u'
key[5] = 'j'
key[6] = 'm'
key[7] = 'n'

answer = [0xae, 0x9e, 0xff, 0x9c, 0xab, 0xc7, 0xd3, 0x81, 0xe7, 0xee, 0xfb, 0x8a, 0x9d, 0xef, 0x8d, 0xae]
#answer = [0x9cff9eae, 0x81d3c7ab, 0x8afbeee7, 0xae8def9d]

table = string.printable[:-6]

p = Process(["gdb", "./obfuscaxor"])
p.recvuntil("gdb-peda$")
p.sendline("break *0x000055555555609c")
for i in range(offset, 16):
    for c in table:
        key[i] = c
        p.recvuntil("gdb-peda$")
        p.sendline("run")
        p.recvuntil("continue:")
        p.sendline(''.join(key))
        p.recvuntil("gdb-peda$")
        p.sendline("x/16b $rax")
        result = p.recvline()
        result += p.recvline()
        r = re.findall(b"0x([0-9a-f]{2})", result)
        r = r[1:9] + r[10:18]
        if int(r[i], 16) == answer[i]:
            print("Found {}: {}".format(i, key[i]))
            break
    else:
        print("ERROR!!")

print(''.join(key))
