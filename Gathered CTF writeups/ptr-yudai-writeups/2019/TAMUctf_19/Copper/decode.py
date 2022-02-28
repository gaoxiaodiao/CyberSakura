import base64

table = {'l': 'YiqMxpZQz+5dPf+qELowBw==', 's': 'US5MJOeTx6L69iQT3Y8B9g==', ' ': '83jbJmmZc/RUXML8GcGuVg==', '-': 'h8zZvECdaFr730Mgo5EgYQ==', 'a': 'RdGNIA97r2yYuQsdXjbQGA==', '\r': 'S+79/0xJH6oVAqvGSE+Vlw==', 'd': 'vCffRJyLzPpoDVYNvxEtoA==', 't': 'MufXoG4oKY+tLj7TNMzMtQ==', 'e': '9+fXRGjlf3TvpwR6XiqcSw==', '>': 'bIyEa1uO0qUPR+sBqjAJ8g==', 'm': '0bGyNN1VKjWCxituvKDVvg==', 'o': '/Ks7iNV5tZaZT32Epav0CA==', 'n': 'KLVDOWDtxnck6THwQuPfGg==', 'i': 'L2/wiXcz7QQyFdbuDe14+w==', 'r': 'MC9KVKLGfFmxvdr6qNuZpA==', '.': 'gCe+M22NmuwF6cPVKGGoZQ==', 'x': 'wJNrzltAAb7rg/64niXZNg==', '\n': '92fKIeYPq2HyqG8DSo2Mfw==', 'c': 'XpjdNQ+r0XfWy25TW5lyAg==', 'h': '4iLXaYY1As8N9+wW+PVQOg==', '"': 'WSThaqht6loKlvNDraoarw==', '=': 'Tkb8E728rfsc+V1i5HtOzQ==', 'p': 'lwzGU75ZfX1C+vFQE1ahTQ==', 'u': 'mJoY/dqOlVLjsIzq/ZmGbg==', 'f': 'qgZnSf9/KcpMFM90/ZaklQ==', '/': 'pxsE18FW3UofpVPzG1RchA==', 'g': 'lwA3zobBmueRmJyafjFH9A=='}

result = input()
data = map(lambda x: x+"==", result.split("=="))
res = ""
for block in data:
    for key in table:
        if block == table[key]:
            res += key
print(res)
