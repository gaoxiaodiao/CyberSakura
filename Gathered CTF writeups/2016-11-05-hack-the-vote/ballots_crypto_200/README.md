# Boxes of ballots (crypto 200)


###ENG
[PL](#pl-version)

In the task we get access to some AES-CBC encryption service.
There was some debug mode avaialble which apparently could be used to extract some of the server code, but this was totally unnecessary.
If we send some payload we get encrypted results.
It's quite easy to notice that we get much more data, which means there has to be prefix or suffix added to our data.
It can't be just PKCS padding because padding never exceeds a single block, and here we had more.

We quickly realise that there is no prefix to the data, simply by observing when encrypted block gets "fixed".
It happens after we provide exactly 16 bytes (so a full block), which means there can be no static prefix.
If there was some static prefix added, the block would get a "fixed" value after providing less characters (until the block boundary is filled).

So we have a long suffix added to the payload before encryption.
It's quite clear that we should check this suffix.
We wrote about this a few times, and the technique is quite basic: 

1. We send data so that first character of padding is the last character in a certain block.
2. We remember the encrypted version of this block (which is [AAAA...AAS] where S is the secret padding byte)
3. We encrypt many blocks with this last byte set to different values, so [AAAA...AAa], [AAAA...AAb], [AAAA...AAc]...
4. If the block from 2) matches block from 3) it means we know the value of the secret byte!
5. We perform this again, this time sending our random filling bytes shorter by 1 byte, so that we get encrypted [AAAA...AAKS] where K is the padding byte we already know from 4) and S is another secret byte we want to know.

We used a script:

```python
import socket
import string

import sys
from flask import json

url = "boxesofballots.pwn.republican"
port = 9001
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((url, port))


def blackbox_encrypt(data):
    data = '{"op": "enc", "data": "' + data + '"}'
    s.sendall(data + "\n")
    result = s.recv(9999)
    loaded = json.loads(result)
    return loaded['data']


def chunk(input_data, size):
    return [input_data[i * size:(i + 1) * size] for i in range(len(input_data) / size)]


if __name__ == "__main__":
    suffix = ""
    for i in range(63 - len(suffix), 0, -1):
        data = 'A' * i
        correct = chunk(blackbox_encrypt(data), 32)[3]
        for c in '{' + "}" + "_" + string.letters + string.digits:
            test = data + suffix + c
            try:
                encrypted = chunk(blackbox_encrypt(test), 32)[3]
                if correct == encrypted:
                    suffix += c
                    print('FOUND', 63 - i, c)
                    if c == "}":
                        print(suffix)
                        sys.exit()
                    break
            except:
                pass
    print(suffix)
```

And got the flag: `flag{Source_iz_4_noobs}`

###PL version

W zadaniu dostajemy dost??p do serwera szyfruj??cego AES-CBC.
Dost??pny by?? jakis debug mode kt??ry pozwala?? pozna?? cz?????? kodu serwera za pomoc?? wywo??ywania b????d??w, ale nie by??o nam to w og??le potrzebne.
Je??li wy??lemy jakie?? dane, otrzmujemy szyfrogram.
??atwo zauwa??y??, ??e dostajemy du??o wi??cej danych ni?? wys??ali??my, wi??c musi by?? dodany jaki?? prefix/suffix.
Nie mo??e to by?? sam padding PKCS bo ten nigdy nie przekracza 1 bloku, a u nas by??o wi??cej.

Szybko zauwa??amy, ??e nie mo??e tam by?? ??adnego statycznego prefixu, poprzez obserwacje kiedy dany blok jest "ustalony".
Dzieje si?? tak, dok??adnie po wys??aniu 16 bajt??w (wi??c ca??ego bloku) co oznacza, ??e nie ma miejsca na sta??y prefix.
Gdyby by?? taki prefix, blok by??by "ustalony" wcze??niej (kiedy blok by si?? dope??ni??).

Mamy wi??c d??ugi suffix dodany do danych przed szyfrowaniem.
To do???? jasne, ??e mamy ten suffix odzyska??.
Pisali??my o tym kilka razy i technika jest do???? prosta:

1. Wysy??amy dane tak ??eby pierwszy bajt paddingu by?? ostatnim znakiem w pewnym bloku.
2. Pami??tamy zaszyfrowan?? wersje tego konkretnego bloku (czyli [AAAA...AAS] gdzie S to sekretny znak paddingu)
3. Szyfrujemy wiele blok??w z ostatnim bajtem ustawionym na r????ne warto??ci, wi??c [AAAA...AAa], [AAAA...AAb], [AAAA...AAc]...
4. Je??li blok z 2) pokrywa si?? z blokiem z 3) oznacza to ??e znamy sekretny bajt!
5. Powtarzamy to kolejny raz, tym razem skracaj??c nasz payload o 1 znak wi??c dostajemy szyfrogram dla [AAAA...AAKS] gdzie K to bajt kt??ry ju?? znamy z 4) a S to kolejny sekretny bajt kt??ry chcemy pozna??.ret byte we want to know.

U??yli??my skryptu:

```python
import socket
import string

import sys
from flask import json

url = "boxesofballots.pwn.republican"
port = 9001
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((url, port))


def blackbox_encrypt(data):
    data = '{"op": "enc", "data": "' + data + '"}'
    s.sendall(data + "\n")
    result = s.recv(9999)
    loaded = json.loads(result)
    return loaded['data']


def chunk(input_data, size):
    return [input_data[i * size:(i + 1) * size] for i in range(len(input_data) / size)]


if __name__ == "__main__":
    suffix = ""
    for i in range(63 - len(suffix), 0, -1):
        data = 'A' * i
        correct = chunk(blackbox_encrypt(data), 32)[3]
        for c in '{' + "}" + "_" + string.letters + string.digits:
            test = data + suffix + c
            try:
                encrypted = chunk(blackbox_encrypt(test), 32)[3]
                if correct == encrypted:
                    suffix += c
                    print('FOUND', 63 - i, c)
                    if c == "}":
                        print(suffix)
                        sys.exit()
                    break
            except:
                pass
    print(suffix)
```

I dostali??my flag??: `flag{Source_iz_4_noobs}`
