##UNIX ONLY

import string
import subprocess
from pwn import *

target = b"""dWWW=- dWWMWWWWWMWMb dMMWWWWWWWWWb -=MMMb
dWMWP dWWWMWWWMMWMMMWWWWWMMMMMMWMMMWWWMMMb qMWb
WMWWb dMWWMMMMMMWWWWMMWWWMWWWWWWMMWWWWMWMWMMMWWWWb dMMM
qMMWMWMMMWMMWWWMWMMMMMMMMWMMMMWWWMMWWMWMWMMWWMWWWWMWWMMWMMWP
QWWWWWWWMMWWWWWWWMMWWWWMMWP QWWWMWMMMMWWWWWMMWWMWWWWWWMP
QWMWWWMMWWMWMWWWWMWWP QWWMWWMMMWMWMWWWWMMMP
QMWWMMMP QMMMMMMP""".replace(b" ", b"").replace(b"\n", b"")

flag = ""

def matchlen(res):
    counter = 0
    for i in range(len(target)):
        if res[i] == target[i]:
            counter += 1
        else:
            return counter

    print("DONE")
    return counter

context.log_level = "ERROR"
current_matchlen = 0

def add_char(current_matchlen, flag):
    for c in string.printable: #"y@ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz}0123456789@_! ":
        print(["/bin/sh", "-c", './papa_bear %s' % (flag + c)])
        res = process(["/bin/sh", "-c", './papa_bear %s' % sh_string(flag + c)]).recvall().replace(b"\t",b"").replace(b" ", b"")[295:].replace(b"\n", b"")
        print(target)
        print(res)

        m = matchlen(res)
        print (m, current_matchlen)
        if m > current_matchlen:
            print (target)
            print (res)
            if m == len(res):
                print(flag + c)
                return
            print(flag + c)
            add_char(m, flag + c)

add_char(10, "CyberEdu{")