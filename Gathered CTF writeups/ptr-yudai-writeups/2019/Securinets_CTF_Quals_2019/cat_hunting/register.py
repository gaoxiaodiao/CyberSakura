import requests

payload = {
    "registration": "",
    "username": "taro",
    "email": "tarotanaka@yopmail.com",
    "password": "tanaka123",
    "button": ""
}
r = requests.post("http://99.80.68.141/index.php", data=payload)
print(r.headers)
print(r.text)
