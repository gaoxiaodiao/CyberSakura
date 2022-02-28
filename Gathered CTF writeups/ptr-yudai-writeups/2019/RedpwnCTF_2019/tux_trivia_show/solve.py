from ptrlib import *
import requests
import json
import re

sock = Socket("chall2.2019.redpwn.net", 6001)

x = sock.recvline()
i = 0
for i in range(1000):
    x = sock.recvline(timeout=1)
    if x is None:
        print(sock.recv())
        break
    r = re.findall(b"What is the capital of (.+)\?", x)
    if not r:
        print(x)
        break
    else:
        country = bytes2str(r[0]).lower()
    r = requests.get("https://restcountries.eu/rest/v2/name/{}".format(country))
    x = json.loads(r.text)
    if isinstance(x, list):
        capital = x[0]["capital"]
    else:
        with open("states.csv", "r") as f:
            for line in f:
                x = line.split(",")
                if x[0].lower() == country:
                    capital = x[1]
                    break
            else:
                capital = "?"
    if country == "kiribati":
        capital = "Tarawa"
    elif country == "democratic republic of the congo":
        capital = "Kinshasa"
    elif country == "east timor (timor-leste)":
        capital = "Dili"
    elif country == "republic of the congo":
        capital = "Brazzaville"
    elif country == "north korea":
        capital = "Pyongyang"
    elif country == "georgia":
        capital = "Atlanta"
    elif country == "south korea":
        capital = "Seoul"
    elif country == "guinea":
        capital = "Conakry"
    elif country == "cape verde":
        capital = "Praia"
    elif country == "india":
        capital = "New Delhi"
    elif country == "samoa":
        capital = "Apia"
    elif country == "moldova":
        capital = "Chisinau"
    elif country == "sudan":
        capital = "Khartoum"
    if "City of " in capital:
        capital = capital.replace("City of ", "")
    print(i, country, capital)
    sock.sendline(capital)
    x = sock.recvline()
    if b'Correct' not in x:
        print(x)
        break
    x = sock.recvline()
    if x:
        print(x)
        break
    i += 1

sock.interactive()
