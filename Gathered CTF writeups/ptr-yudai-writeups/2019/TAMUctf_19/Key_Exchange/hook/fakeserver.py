from ptrlib import *
import base64
import sys
import socket
from DiffieHellman import DiffieHellman
from AESCipher import AESCipher
import time

dh = DiffieHellman()
pka = dh.publicKey

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("172.30.0.14", 8080))
s.listen(1)

script = {
    b'1st Soldier with a Keen Interest in Birds: Who goes there?\n': b'King Arthur: It is I, Arthur, son of Uther Pendragon, from the castle of Camelot. King of the Britons, defeater of the Saxons, Sovereign of all England!\n',
    b'1st Soldier with a Keen Interest in Birds: Pull the other one!\n': b'King Arthur: I am, and this is my trusty servant Patsy. We have ridden the length and breadth of the land in search of knights who will join me in my court at Camelot. I must speak with your lord and master.\n',
    b'1st Soldier with a Keen Interest in Birds: What? Ridden on a horse?\n': b'King Arthur: Yes!\n',
    b"1st Soldier with a Keen Interest in Birds: You're using coconuts!\n": b'King Arthur: What?\n',
    b"1st Soldier with a Keen Interest in Birds: You've got two empty halves of coconut and you're bangin' 'em together.\n": b'King Arthur: So? We have ridden since the snows of winter covered this land, through the kingdom of Mercia, through...\n',
    b"1st Soldier with a Keen Interest in Birds: Where'd you get the coconuts?\n": b'King Arthur: We found them.\n',
    b"1st Soldier with a Keen Interest in Birds: Found them? In Mercia? The coconut's tropical!\n": b'King Arthur: What do you mean?\n',
    b'1st Soldier with a Keen Interest in Birds: Well, this is a temperate zone.\n': b'King Arthur: The swallow may fly south with the sun or the house martin or the plover may seek warmer climes in winter, yet these are not strangers to our land?\n',
    b'1st Soldier with a Keen Interest in Birds: Are you suggesting coconuts migrate?\n': b'King Arthur: Not at all. They could be carried.\n',
    b'1st Soldier with a Keen Interest in Birds: What? A swallow carrying a coconut?\n': b'King Arthur: It could grip it by the husk!\n',
    b"1st Soldier with a Keen Interest in Birds: It's not a question of where he grips it! It's a simple question of weight ratios! A five ounce bird could not carry a one pound coconut.\n": b"King Arthur: Well, it doesn't matter. Will you go and tell your master that Arthur from the Court of Camelot is here?\n",
    b'1st Soldier with a Keen Interest in Birds: Listen. In order to maintain air-speed velocity, a swallow needs to beat its wings forty-three times every second, right?\n': b'King Arthur: Please!\n',
    b'1st Soldier with a Keen Interest in Birds: Am I right?\n': b'King Arthur: I suppose so. Here is your flag: gigem{d1ff13_w1ff13_b6dffb749778d6b}\n'
}

while True:
    c, addr = s.accept()
    while True:
        data = c.recv(4096)
        pkb = int(base64.b64decode(data))
        print(pkb)
        dh.genKey(pkb)
        c.send(base64.b64encode(str2bytes(str(pka))))
        aes = AESCipher(dh.getKey())
        # Hello
        while True:
            # Receive
            data = c.recv(4096)
            plain = aes.decrypt(data)
            print(plain)
            if plain not in script:
                exit(1)
            # Send
            c.send(aes.encrypt(bytes2str(script[plain])))
    c.close()
