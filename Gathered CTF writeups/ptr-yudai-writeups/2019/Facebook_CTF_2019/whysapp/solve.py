from Crypto.Cipher import AES
import base64
import random
from ptrlib import *

key = "yeetyeetyeetyeet"
crypto = AES.new(key, AES.MODE_ECB)

flag = False
def process(cipher, rid=1):
    global flag
    plain = crypto.decrypt(base64.b64decode(cipher)).rstrip(b"\x00")
    plain = bytes2str(plain)
    #dump("<<< " + plain)
    
    r = 0
    #r = random.randint(1, 1000000000)
    try:
        ope, data = plain.split(":")
    except:
        print(plain)
        exit()

    if flag and ope == 'msg':
        dump("Attempt: " + str(rid))
        if "You're not zuck!!!!!!!!" not in data:
            dump(data)

    if ope == 'math':
        # math
        result = eval(data)
        plain = "{}:{}:{}".format(r, "math", result)
    elif ope == 'ping':
        # ping
        plain = "{}:ping:pong".format(r)
    elif ope == 'flag':
        # flag
        plain = "{}:flag:{}".format(rid, data) # ?????
        flag = True
    else:
        # cats
        plain = "{}:{}".format(r, plain)
    #dump(">>>" + plain)
    
    plain += "\x00" * (16 - (len(plain) % 16))
    cipher = base64.b64encode(crypto.encrypt(plain))
    return cipher

log.level = ["warning"]
for r in range(4, 0x100000000):
    sock = Socket("challenges.fbctf.com", 4001)
    flag = False
    while True:
        c = sock.recv()
        if c is None:
            break
        s = process(c, r)
        sock.sendline(s)
    sock.close()
