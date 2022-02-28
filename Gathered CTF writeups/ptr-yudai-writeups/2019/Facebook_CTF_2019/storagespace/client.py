from ptrlib import *
import json
import base64
import re
from fastecdsa.curve import Curve
from fastecdsa.point import Point
import hashlib
import sys
import time

def sign(payload):
    sign_payload = {"command": "sign", "params":{
    "command": payload["command"], "params": payload["params"]
    }}
    sock.recv()
    sock.sendline(json.dumps(sign_payload))
    w = sock.recvline()
    s = json.loads(w.rstrip())
    return s

def info():
    payload = {"command": "info", "params": {}}
    payload["sig"] = sign(payload)["sig"]
    sock.recv()
    sock.sendline(json.dumps(payload))
    curve = sock.recvline().rstrip()
    generator = sock.recvline().rstrip()
    pubkey = sock.recvline().rstrip()
    r = re.findall(b"curve: y\*\*2 = x\*\*3 \+ (\d+)\*x \+ (\d+) \(mod (\d+)\)", curve)
    curve = (int(r[0][0]), int(r[0][1]))
    prime = int(r[0][2])
    r = re.findall(b"generator: \((\d+), (\d+)\)", generator)
    G = (int(r[0][0]), int(r[0][1]))
    r = re.findall(b"public key: \((\d+), (\d+)\)", pubkey)
    pubkey = (int(r[0][0]), int(r[0][1]))
    return curve, prime, G, pubkey

def spec(mode="all"):
    payload = {"command": "spec", "params": {"mode": mode}}
    payload["sig"] = sign(payload)["sig"]
    sock.sendline(json.dumps(payload))
    print(bytes2str(sock.recv()))
    print(bytes2str(sock.recv()))
    print(bytes2str(sock.recv()))
    exit()

def save(name, flag):
    payload = {"command": "save","params": {"name": name, "flag": flag}}
    payload["sig"] = sign(payload)["sig"]
    sock.recv()
    sock.sendline(json.dumps(payload))
    sock.recvuntil("flag stored\n")

def list():
    payload = {"command": "list", "params": {}}
    payload["sig"] = sign(payload)["sig"]
    sock.recv()
    sock.sendline(json.dumps(payload))
    res = sock.recv()
    return res.split(b"\n")[:-1]

if __name__ == '__main__':
    fake_payload = {"command": "flag", "params": {"name": "fbctf"}}
    fake_msg = json.dumps(fake_payload, sort_keys=True)
    
    sock = Socket("challenges.fbctf.com", 8089)
    sock.recvuntil("patience\n")
    param, n, G, H = info()
    curve = Curve(
        name = "taro",
        p = n,
        q = n,
        a = param[0],
        b = param[1],
        gx = G[0],
        gy = G[1]
    )
    G = Point(G[0], G[1], curve=curve)
    H = Point(H[0], H[1], curve=curve)
    dump("curve: y^2 = x^3 + {}x + {} mod {}".format(param[0], param[1], n))
    dump("G = ({}, {})".format(G.x, G.y))
    dump("H = ({}, {})".format(H.x, H.y))
    payload = {"command": "help", "params": {}}
    l = base64.b64decode(sign(payload)["sig"]).split(b"|")
    r, s = int(l[0]), int(l[1])
    dump("r, s = {}, {}".format(s, r))
    dump("new_msg = " + fake_msg)
    with open("input.txt", "w") as f:
        f.write("{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format(n, param[0], param[1], s, r, G.x, G.y, H.x, H.y))
    while True:
        try:
            sig = sys.stdin.readline().rstrip()
            if sig:
                break
        finally:
            time.sleep(1)
    dump("sig = " + sig)
    payload = {"command": "flag", "params": {"name": "fbctf"}, "sig": sig}
    sock.recv()
    sock.sendline(json.dumps(payload))
    print(sock.recv())
    
    sock.interactive()
