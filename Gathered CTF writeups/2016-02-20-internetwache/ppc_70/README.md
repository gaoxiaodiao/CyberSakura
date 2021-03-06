## A numbers game II (PPC/Crypto, 70p)

	Description: Math is used in cryptography, but someone got this wrong. Can you still solve the equations? 
	Hint: You need to encode your answers. 
	
###ENG
[PL](#pl-version)

Server sends input as:

	Hi, I like math and cryptography. Can you talk to me?!
	Level 1.: 4.4.5.3.3.3.3.3.3.3.6.4.3.3.3.3.3.4.3.4.3.4.3.3.3.3.3.3.3.4.6.4.3.3.3.3.3.3.6.4.3.4.4.5
	
And we are also given the encryption code:

```python
    def encode(self, eq):
        out = []
        for c in eq:
            q = bin(self._xor(ord(c),(2<<4))).lstrip("0b")
            q = "0" * ((2<<2)-len(q)) + q
            out.append(q)
        b = ''.join(out)
        pr = []
        for x in range(0,len(b),2):
            c = chr(int(b[x:x+2],2)+51)
            pr.append(c)
        s = '.'.join(pr)
        return s
```

The goal is to decrypt the task, solve it and then send encrypted answer.
First we split the encryption into two functions (one loop in each) and then wrote decryption for each one of them.
We replaced constants like (2<<4) for their numeric values for readibility.

First part of the encryption function takes each character of the input, xors it with static key 32, converts this to binary and add 0 padding so that this binary representation has always 8 digits.

Therefore for the decryption we can simply slice the input to get 8-digit long binary strings, then we treat each one of them as integers in base-2 (this gets rid of 0 padding) and xor with static key 32 (since `a xor b xor b = a`).

```python
def encode1(eq):
    out = []
    for c in eq:
        q = bin((ord(c) ^ 32)).lstrip("0b")
        q = "0" * (8 - len(q)) + q
        out.append(q)
    b = ''.join(out)
    return b


def decode1(b):
    result = []
    for i in range(0, len(b), 8):
        q = b[i:i + 8]
        q = chr(int(q, 2) ^ 32)
        result.append(q)
    return "".join(result)
```

Second part of encryption takes the binary string we got from the first part, then slices it into 2-digit parts, treats each one as integer in baes-2, adds 51 and casts this to char. Then all chars are concatenated with dot as separator.

Therefore the decryption of this part splits the input by dot to get characters, then casts the char to integer and subtracts 51, converts the result to 2-digit long binary number and then joins all those numbers into a single string.

```python
def encode2(b):
    pr = []
    for x in range(0, len(b), 2):
        c = chr(int(b[x:x + 2], 2) + 51)
        pr.append(c)
    s = '.'.join(pr)
    return s


def decode2(task):
    return "".join("{0:02b}".format((ord(c) - 51)) for c in task.split("."))
```

With this we can now decode the input, which turns out to be exactly the same as for previous task `A numbers game`, so we use the same procedure to solve the tasks, and we use the provided `encrypt()` function to send responses. Complete code is in [here](decrypter.py)

After 100 tasks we get the flag: `IW{Crypt0_c0d3}`

###PL version

Serwer przysy??a dane w formacie:

	Hi, I like math and cryptography. Can you talk to me?!
	Level 1.: 4.4.5.3.3.3.3.3.3.3.6.4.3.3.3.3.3.4.3.4.3.4.3.3.3.3.3.3.3.4.6.4.3.3.3.3.3.3.6.4.3.4.4.5
	
Dostajemy te?? kod procedury szyfruj??cej:

```python
    def encode(self, eq):
        out = []
        for c in eq:
            q = bin(self._xor(ord(c),(2<<4))).lstrip("0b")
            q = "0" * ((2<<2)-len(q)) + q
            out.append(q)
        b = ''.join(out)
        pr = []
        for x in range(0,len(b),2):
            c = chr(int(b[x:x+2],2)+51)
            pr.append(c)
        s = '.'.join(pr)
        return s
```

Zadanie polega na zdekodowaniu wej??cia, rozwi??zaniu problemu a nast??pnie wys??aniu zakodowanej odpowiedzi.
Na pocz??tku podzielili??my funkcje szyfruj??c?? na kawalki (jedna p??tla w kawa??ku) a nast??pnie napisali??my kod odwracajacy te funkcje.
Podmienili??my sta??e jak (2<<4) na ich warto???? numeryczn?? dla poprawnienia czytelno??ci.

Pierwsza cz?????? szyfrowania bierze ka??dy znak z wej??cia, xoruje go ze statycznym kluczem 32, zamienia uzyskan?? liczb?? na binarn?? i dodaje padding 0 tak ??eby liczba zawsze mia??a 8 cyfr.

W zwi??zu z tym deszyfrowanie polega na podzieleniu wej??cia na 8-cyfrowe ci??gi binarne, potraktowanie ka??dego jako integer o podstawie 2 (to automatycznie za??atwia spraw?? paddingu) i xorowaniu tej liczby z 32 (poniewa?? `a xor b xor b = a`).

```python
def encode1(eq):
    out = []
    for c in eq:
        q = bin((ord(c) ^ 32)).lstrip("0b")
        q = "0" * (8 - len(q)) + q
        out.append(q)
    b = ''.join(out)
    return b


def decode1(b):
    result = []
    for i in range(0, len(b), 8):
        q = b[i:i + 8]
        q = chr(int(q, 2) ^ 32)
        result.append(q)
    return "".join(result)
```

Druga cz?????? szyfrowania bierze binarny ci??g uzyskany w cz????ci pierwszej, dzieli go na 2-cyfrowe fragmenty, traktuje ka??dy jako integer o podstawie 2, dodaje 51 i rzutuje to na char. Nast??pnie wszystkie chary s?? sklejane z kropk?? jako separatorem.

W zwi??zku z tym deszyfrowanie tej cz????ci polega na podzieleniu wej??cia po kropkach aby uzyska?? chary, nast??pnie rzutowanie tych char??w na integery, odj??ciu od nich 51, zamiany wyniku na 2-cyfrow?? liczb?? binarn?? a nast??pnie sklejenie tych liczb w jeden ci??g.

```python
def encode2(b):
    pr = []
    for x in range(0, len(b), 2):
        c = chr(int(b[x:x + 2], 2) + 51)
        pr.append(c)
    s = '.'.join(pr)
    return s


def decode2(task):
    return "".join("{0:02b}".format((ord(c) - 51)) for c in task.split("."))
```

Dzi??ki temu mo??emy teraz odkodowa?? wej??cie, kt??re okazuje si?? mie?? taki sam format jak w zadaniu `A numbers game`, wi??c wykorzystujemy identyczny kod do rozwi??zania problemu a wynik przesy??amy szyfruj??c go dan?? metod?? `encrypt()`. Ca??y kod rozwi??zania znajduje si?? [tutaj](decrypter.py).

Po 100 zadaniach dostajemy flag??: `IW{Crypt0_c0d3}`
