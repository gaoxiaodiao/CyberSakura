from ptrlib import *
import base64
from DiffieHellman import DiffieHellman
from AESCipher import AESCipher

dh = DiffieHellman()
pka = base64.b64encode(str2bytes(str(dh.publicKey)))

sock = Socket("172.30.0.2", 5005)

# Hello
sock.send(pka)
data = sock.recv()
pkb = int(base64.b64decode(data))
dh.genKey(pkb)

msglist = [
    b'1st Soldier with a Keen Interest in Birds: Who goes there?\n',
    b'1st Soldier with a Keen Interest in Birds: Pull the other one!\n',
    b'1st Soldier with a Keen Interest in Birds: What? Ridden on a horse?\n',
    b"1st Soldier with a Keen Interest in Birds: You're using coconuts!\n",
    b"1st Soldier with a Keen Interest in Birds: You've got two empty halves of coconut and you're bangin' 'em together.\n",
    b"1st Soldier with a Keen Interest in Birds: Where'd you get the coconuts?\n",
    b"1st Soldier with a Keen Interest in Birds: Found them? In Mercia? The coconut's tropical!\n",
    b'1st Soldier with a Keen Interest in Birds: Well, this is a temperate zone.\n',
    b'1st Soldier with a Keen Interest in Birds: Are you suggesting coconuts migrate?\n',
    b'1st Soldier with a Keen Interest in Birds: What? A swallow carrying a coconut?\n',
    b"1st Soldier with a Keen Interest in Birds: It's not a question of where he grips it! It's a simple question of weight ratios! A five ounce bird could not carry a one pound coconut.\n",
    b'1st Soldier with a Keen Interest in Birds: Listen. In order to maintain air-speed velocity, a swallow needs to beat its wings forty-three times every second, right?\n',
    b'1st Soldier with a Keen Interest in Birds: Am I right?\n'
]

# OK
aes = AESCipher(dh.getKey())
for msg in msglist:
    cipher = aes.encrypt(bytes2str(msg))
    sock.send(cipher)
    data = sock.recv()
    if data is None:
        break
    plain = aes.decrypt(data)
    print(plain)
