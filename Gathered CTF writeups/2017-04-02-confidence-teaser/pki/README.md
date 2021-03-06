# Public Key Infrastructure (crypto)

## ENG
[PL](#pl-version)

In the task we get [code](task.py) running on the server.

We can "register" a new user, and for given `login name` and set of binary bytes `n` we get RSA-encrypted with `(65537, n)` digital signature of string `'MSG = {n: ' + n + ', name: ' + name + '}'`.
Bytes `n` are simply casted to int.

We can also "login" by providing `login name`, `n` and a proper signature, and this will give us the flag if we login as `admin`.
Obviously we can't register "admin" and there is no way around the check here.

The Digital Signature Algorithm is implemented with no issues here, so there is no vulnerability there.
It took us a while to figure out the mistake and how to exploit it.
The problem in the code is here:

```python
def makeK(name, n):
  return 'K = {n: ' + n + ', name: ' + name + ', secret: ' + SECRET + '}'
```

Value `k` should be secret and unpredictable for every signature, because if we can obtain 2 signatures with the same `k`, we can very simply recover the value of `k`.
In our case this condition is not really fulfilled, because md5 algorithm is prone to collisions.
It it also Merkle-Damgard hash prone to length extension, and therefore if we can get a collision on two inputs, the hash values will stay the same even if we add more data at the end, as long as we add the same data.
This means that if we can find a collision on prefix `'K = {n: ' + n` for two different `n` values, we will get identical `k` values (if we use the same `name`) because the suffixes are always the same.

We used `fastcoll/hashclash` to generate the collisions for the prefix `'K = {n: ' + n` with random bytes as `n` value.

There is, however, one slight issue -> we actually can't use a totally random `n` value!
After all the server is using this value for RSA encryption of the signature, so if we can't factor `n` we won't be able to decrypt the signature we need.
Therefore, we wrote a simple script which was checking the `n` values we got in the collision in factordb to make sure it is factored:

```python
def is_ok(data):
	if data.strip() == "CF *":
		return False
	if data.strip() == "CF":
		return False
	return True

def check_n(file):
	payload = open("colisions/"+file, "rb").read()[8:]
	n = int(payload.encode('hex'), 16)
	r = get(url="https://factordb.com/index.php?query="+str(n))	
	soup = BeautifulSoup(r.text)
	data = soup.getText().split("\n")
	return is_ok(data[data.index('Result:')+4])
```

With this after a while we manage to get two nice collisions with proper `n` values: [col1](col1), [col2](col2).

They both are fully factored in factordb so we get factors:

```
factors1 = [234616432627, 705869477985961204313551643916777744071330628233585786045998984992545254851001542557142933879996265894077678757754161926225017823868556053452942288402098017612976595081470669501660030315795007199720049960329731910224810022789423585714786440228952065540955255662140767866791612922576360776884260619L]

factors2 = [119851, 236017, 5854608817710130372948444562294396040006311067115965740712711205981029362712183315259168783815905208719000197236691607700100836391807927746833977891792631066541406816904680111217125634549418611669208807316369565620310660295144628581977856740654199823679135895590513942858128229967305158632385155587L]
```

With this we can use standard RSA for first one, and multiprime RSA for the second one, and decode the signatures from the server.
The signature is a pair `(s,r)` or in our case a single value `r*Q + s` which can be easily split into `s` and `r` by div and mod.

Directly from the way the value `s` is calcualted  we have:

```
s_1 = modinv(k,q) * (H(msg_1) + private_key*r) mod q
s_2 = modinv(k,q) * (H(msg_2) + private_key*r) mod q
```

We can transform this further:

```
(s_1 - s_2) modq = (modinv(k,q) * (H(msg_1) + private_key*r) - modinv(k,q) * (H(msg_2) + private_key*r)) modq
```

then:

```
(s_1 - s_2) modq = modinv(k,q) * (H(msg_1) + private_key*r - H(msg_2) - private_key*r) modq
```

which removes the unknown `private_key*r` part leaving:

```
(s_1 - s_2) modq = modinv(k,q) * H(msg_1) - H(msg_2) modq
```

And therefore we get the equation for `k`:

```
k modq = ((H(msg_1) - H(msg_2)) * modinv((s_1 - s_2), q)) modq
```

If we have `k` we can easily recover the `private_key` again transforming the equation:

```
s = modinv(k,q) * (H(msg) + private_key*r) mod q
```

because now we know all the values, so we can transform this to:

```
private_key = ((s * k) - H(m)) * modinv(r, q)
```

Now if we have the private key we can sign any message we want.
Keep in mind that the value of `SECRET` which server uses to calculate `k` is not needed for us at all.
The value of `k` can be any number, so we can make:

```python
def simple_sign(name, n, priv):
    k = 5 # why not? ;)
    r = pow(G, k, P) % Q
    s = (modinv(k, Q) * (h(makeMsg(name, n)) + priv * r)) % Q
    return r * Q + s
```

And this will give us the proper signature for the data.
We calculate `admin_sig = simple_sign("admin", "1", private_key)`, and login with it to get the flag:

`DrgnS{ThisFlagIsNotInterestingJustPasteItIntoTheScoreboard}`

The whole solver script is [here](solver.py)

## PL version

W zadaniu dostajemy [kod](task.py) dzia??aj??cy na serwerze.

Mo??emy "zarejestrowa??" nowego u??ytkownika, a dla danego `loginu` oraz pewnych danych binarnych `n` dostaniemy zaszyfrowane za pomoc?? RSA z `(65537, n)` cyfrowy podpis dla stringa `'MSG = {n: ' + n + ', name: ' + name + '}'`.
Bajty `n` s?? tutaj zwyczajnie rzutowane do inta.

Mo??emy tak??e "zalogowa??" si?? podaj??c `login`, `n` oraz poprawny podpis i to da nam flag?? je??li zalogujemy si?? jako `admin`.
Oczywi??cie nie mo??emy zarejestrowa?? loginu "admin" i nie ma da si?? tego obej????.

Digital Signature Algorithm jest tu zaimplementowan bez widocznych b????d??w ani r????nic, wi??c nie ma tam ??adnej podatno??ci.
Zaj????o nam troch?? czasu znalezienie luki i wymy??lenie jak j?? wykorzysta??.
Problem jest tutaj:

```python
def makeK(name, n):
  return 'K = {n: ' + n + ', name: ' + name + ', secret: ' + SECRET + '}'
```

Warto???? `k` powinna by?? sekretna i nieprzewidywalna dla ka??dego podpisu, poniewa?? je??li jeste??my w stanie uzyska?? 2 podpisy z tym samym `k`, mo??emy ??atwo wyliczy?? `k`.
W naszym przypadku ten warunek nie jest spe??niony bo md5 jest podatne na kolizje.
Jest to takze hash konstrukcji Merkle-Damgard podatny na length extension a to oznacza, ??e je??li uzyskamy kolizje dla pewnych dw??ch zbior??w danych wej??ciowych to warto???? hasha md5 dla nich b??dzie r??wna nawet je??li dodamy na koniec jakie?? dane, o ile dodajemy te same dane.
To oznacza ??e je??li znajdziemy kolizje dla prefixu `'K = {n: ' + n` dla dw??ch r????nych warto??ci `n` to uzyskamy identyczne warto??ci `k` dla nich (je??li u??ywamy takiego samego `name`), bo suffixy s?? takie same.

U??yli??my `fastcoll/hashclash` do generowania kolizji dla prefixu `'K = {n: ' + n` z losowymi bajtami jako `n`.

Jest tutaj jednak pewien problem -> nie mo??emy u??y?? zupe??nie dowolnego `n`!
Nale??y pami??ta??, ??e serwer odsy??a nam podpis zaszyfrowany przez RSA z u??yciem `n`, wi??c je??li nie umiemy sfaktoryzowa?? `n` to nie b??dziemy mogli zdekodowa?? podpisu.
W zwi??zku z tym napisali??my skrypt kt??ry sprawdza?? w factordb warto??ci `n` dla kt??rych dostali??my kolizje, zeby upewni?? si??, ??e mamy dla nich faktoryzacje:

```python
def is_ok(data):
	if data.strip() == "CF *":
		return False
	if data.strip() == "CF":
		return False
	return True

def check_n(file):
	payload = open("colisions/"+file, "rb").read()[8:]
	n = int(payload.encode('hex'), 16)
	r = get(url="https://factordb.com/index.php?query="+str(n))	
	soup = BeautifulSoup(r.text)
	data = soup.getText().split("\n")
	return is_ok(data[data.index('Result:')+4])
```

Dzi??ki temu po pewnym czasie uda??o nam si?? uzyska?? kolizje z pasujacymi `n`: [col1](col1), [col2](col2).

Obie s?? w pe??ni sfaktoryzowane:

```
factors1 = [234616432627, 705869477985961204313551643916777744071330628233585786045998984992545254851001542557142933879996265894077678757754161926225017823868556053452942288402098017612976595081470669501660030315795007199720049960329731910224810022789423585714786440228952065540955255662140767866791612922576360776884260619L]

factors2 = [119851, 236017, 5854608817710130372948444562294396040006311067115965740712711205981029362712183315259168783815905208719000197236691607700100836391807927746833977891792631066541406816904680111217125634549418611669208807316369565620310660295144628581977856740654199823679135895590513942858128229967305158632385155587L]
```

Dzi??ki temu mo??emy u??y?? klasycznego RSA dla pierwszego podpisu i multiprime RSA dla drugiego, ??eby zdekodowa?? podpisy wys??ane przez serwer.

Podpis to para `(s,r)` lub jak w naszym przypadku jedna warto???? `r*Q + s` kt??r?? ??atwo roz??o??y?? na `s` i `r` za pomoc?? dzielenia i reszty z dzielenia przez `Q`.

Bezpo??rednio z tego jak liczymy `s` podczas generowania podpisu mamy:

```
s_1 = modinv(k,q) * (H(msg_1) + private_key*r) mod q
s_2 = modinv(k,q) * (H(msg_2) + private_key*r) mod q
```

Co mo??na przekszta??ci?? do:

```
(s_1 - s_2) modq = (modinv(k,q) * (H(msg_1) + private_key*r) - modinv(k,q) * (H(msg_2) + private_key*r)) modq
```

a nast??pnie upro??ci??:

```
(s_1 - s_2) modq = modinv(k,q) * (H(msg_1) + private_key*r - H(msg_2) - private_key*r) modq
```

Co pozwala pozby?? si?? nieznanej cz????ci `private_key*r`, zostawiaj??c:

```
(s_1 - s_2) modq = modinv(k,q) * H(msg_1) - H(msg_2) modq
```

A ty samym r??wnanie dla `k` to:

```
k modq = ((H(msg_1) - H(msg_2)) * modinv((s_1 - s_2), q)) modq
```

Maj??c `k` mo??emy teraz ??atwo wyliczy?? `private_key`, zn??w przekszta??caj??c r??wnanie dla `s`:

```
s = modinv(k,q) * (H(msg) + private_key*r) mod q
```

Poniewa?? znamy wszystkie parametry mo??emy przekszta??cic to do postaci:

```
private_key = ((s * k) - H(m)) * modinv(r, q)
```

I teraz maj??c wyliczony klucz prywatny mo??emy podpisa?? co tylko chcemy.
Warto pami??ta??, ??e nie potrzebujemy warto??ci `SECRET` za pomoc?? kt??rej serwer oblicza warto???? `k`.
Warto???? `k` mo??e by?? zupe??nie dowolna wi??c mo??emy napisa??:

```python
def simple_sign(name, n, priv):
    k = 5 # why not? ;)
    r = pow(G, k, P) % Q
    s = (modinv(k, Q) * (h(makeMsg(name, n)) + priv * r)) % Q
    return r * Q + s
```

I taka funkcja pozwoli poprawnie podpisywa?? dane.
Obliczamy wi??c `admin_sig = simple_sign("admin", "1", private_key)`, i loguj??c si?? tym podpisem dostajemy flag??:

`DrgnS{ThisFlagIsNotInterestingJustPasteItIntoTheScoreboard}`

Ca??y skrypt solvera jest [tutaj](solver.py)
