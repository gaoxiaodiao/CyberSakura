import requests
import re

cookies = {"name": "papyrus", "password": "papyrus123"}

while True:
    data = {"mine": 1}
    r = requests.post("http://95.179.148.72:8083/index.php", cookies=cookies, data=data)
    rr = re.findall(b"Your USD: <b>(\d+.\d+)</b>", r.text.encode("ascii"))
    usd = rr[0] if rr else 0.0
    rr = re.findall(b"Your BTC: <b>(\d+.\d+)</b>", r.text.encode("ascii"))
    btc = rr[0] if rr else 0.0
    print("USD={} / BTC={}".format(usd, btc))

