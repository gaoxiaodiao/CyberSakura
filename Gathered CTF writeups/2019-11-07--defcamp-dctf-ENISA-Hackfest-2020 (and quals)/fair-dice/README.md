# fair-dice (50pts, 71 solved) Misc & Programming [Easy]

## First look
When we first connect to the server, it explains the rules of the game and we can start. After that it gives us some dices and our goal then is to choose the best dice to win.

## Solving
We can simply parse the dices and find the one with the highest average and throw that one if the bot didn't choose that one yet and as the game progresses add some more simple rules:
```python
from pwn import *
import re

foundFlag = False

while foundFlag == False:
    r = remote("34.89.250.23", 30769)
    r.recvuntil("start?")
    r.sendline("")
    dices = {}

    while True:
        diceData = r.recv()
        try:
            if b"Here is the " in diceData:
                avg = 0
                for num in re.findall(rb'x\s+(\d+)\s+x', diceData):
                    avg += int(num)
            
                avg /= 6

                diceName = re.search(rb"Here is the (\w+) dice", diceData).groups(1)
                dices[diceName] = avg
                r.sendline("")
                continue

            if b"I won" in diceData:
                break
            
            if b"DCTF" in diceData:
                print(diceData)
                foundFlag = True
                break

            if b"Ok?" in diceData:
                r.sendline("")
                continue

            hisChoice = re.search(rb"I am chosing the (\w+) dice!", diceData).groups(0)
            hisDice = dices[hisChoice]
            bestChoice = b""
            for key in dices.keys():
                if key != hisChoice:
                    if bestChoice == b"":
                        bestChoice = key
            
                    if dices[key] > dices[bestChoice]:
                        bestChoice = key

            r.sendline(bestChoice[0])
        except:
            print(diceData)
    r.close()
```
And after a bit, we get our flag: `DCTF{7537c933a266a45500c5bd35f20679539f596df9e706dc95fae22d15b812141f}`