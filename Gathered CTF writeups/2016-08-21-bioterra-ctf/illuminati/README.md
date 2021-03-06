## Illuminati (Web, 200p)

###ENG
[PL](#pl-version)

In the task we get access to a Illuminati recruitment webpage.
However the recruitment is closed and we can only send messages to the admin and he might accept us.
We could see only our own messages.

Our first assumption was that it's some standard XSS attack on the admin, but placing some example XSS payload in the form uncovered an SQL error printed.
This meant we have an SQL Injection vulnerability.
The form had 2 fields:

- subject limited to 40 characters (verified server side)
- message with no length limit

Both of them were exploitable with a `"`.
The injection point was an `INSERT INTO` query, which limited a bit our capabilities.
More so that initially we though we have to exploit the `subject` field doing some crazy SQL golfing in 40 characters, since we could not inject a `select` into the second field due to query construction.
The query was something like:

`insert into requests (id, "$subject", "$message")`

Which means that the message field content was either inside quotation marks, or if we close the quotation mark, already outside insert query.
We could chain another insert values but we didn't know the ID and thus we would not see the contents of this second insert query.

For a moment we though we will have to make a blind sqli here, but fortunately we came up with a great idea - why not chain injections from both fields at the same time, putting an injection in `subject` which will `shift` the column to the `message` field, lifting the 40 characters limit.

We figured we can put for example the subject as:

```
theSubject",concat(
```

and message as:

```
,(select whatever we want)))#
```

And therefore we escape the quotation marks by concat of empty string and our query result!

This way we could now execute any query we wanted, so we dumped the whole database via group_concat and substring.
The passwords, including the admin password, were hashed and not likely to be broken.
Rest of the database did not contain anything particularly useful.

We thought that maybe we could update the admin password to our own password hash (hoping the passwords are not salted with username as salt), but we did not have rights to do it.

It took us a while to notice that the session cookie for this task was very particular - it helped that we developed a simple python script to send queries, and thus we had session cookie as parameter.
The cookie was a number plus our user ID, which is quite odd.
So we figured that maybe it's possible to forge admin cookie.
In the database in users table there was a strange field with `last login timestamp`.
Timestamps are often used as random seeds so we checked what random can we get using our timestamp as seed and we got our missing cookie part!

Therefore, we finally extracted admin login timestamp from database via SQL Injection, we seeded random with the value, took the generated random int, glued it with admin user ID and got the final cookie `1229569179-209`, which was enough to get us logged in as admin and get the flag.

###PL version

W zadaniu dostajemy dost??p do strony rekrutacyjnej Illuminat??w.
Jednak??e rekrutacja jest zamkni??ta i mo??emy jedynie wys??a?? wiadomo???? do admina, kt??ry mo??e nas zaakceptuje.
Mo??emy widzie?? tylko nasze w??asne wiadomo??ci.

Nasze pierwsze skojarzenie to oczywi??cie standardowy atak XSS na admina, jednak??e przyk??adowy payload XSS w formularzu sprawi?? ??e naszym oczom ukaza?? si?? b????d SQLa.
To oznacza??o, ??e podatno???? stanowi jednak SQL Injection.
Formularz mia?? 2 pola:

- temat z limitem 40 znak??w (sprawdzane po stronie serwera)
- wiadomo???? bez limitu d??ugo??ci

Oba pola by??y exploitowalne przez `"`.
Punktem wstrzykni??cia by??o zapytanie `INSERT INTO` co troch?? ogranicza??o nasze mo??liwo??ci.
Dodatkowo pocz??tkowo my??leli??my, ??e mo??emy u??y?? efektywnie tylko pola `subject` i trzeba b??dzie robi?? jaki?? ci????ki SQL golfing na 40 znak??w, poniewa?? nie mogli??my wstrzykn???? `select` do drugiego pola ze wzgl??du  na budow?? zapytania.
Zapytanie mia??o posta??:

`insert into requests (id, "$subject", "$message")`

Co oznacza??o, ??e zawarto???? pola message by??a albo wewnatrz cudzys??ow??w, albo je??li je domkn??li??my, poza danymi do insertowania.
Mogliby??my co prawda do????czy?? kolejny zestaw danych dla insert, ale nie znali??my warto??ci ID i nie mogliby??my zobaczy?? wyniku tego drugiego zapytania.

Pocz??tkowo my??leli??my, ??e sko??czy si?? na ataku blind sqli, ale na szcz????cie wpadli??my na lepszy pomys?? - czemu nie po????czy?? wstrzykni??cia z dw??ch p??l jednocze??nie, umieszczajac w polu `subject` kod kt??ry `przesunie` kolumne do pola `message`, usuwaj??c 40 znakowy limit.

Wymy??lili??my, ??e do pola subject mo??na da??:


```
theSubject",concat(
```

a wiadomo????:

```
,(select whatever we want)))#
```

I tym samym uciekamy z cudzys??owia przez z????czenie pustego stringa z wynikiem naszego zapytania!

W ten spos??b mogli??my teraz wykona?? dowolne zapytania wi??c dumpowali??my ca???? baz?? przez group_concat i substring.
Has??a w bazie, w tym has??o admina, by??y niestety hashowane i raczej nie wygl??da??y na ??amalne.
Reszta bazy nie wygl??da??a na zbyt przydatn??.

My??leli??my, ??e mo??e da si?? podmieni?? hash has??a admina na nasz w??asny (licz??c, ??e has??a nie s?? solone loginami), ale nie mieli??my do tego praw.

Chwile zaj????o nam zauwa??enie, ??e ciastko sesji dla tego zadania wygl??da??o do???? nietypowo - pom??g?? fakt, ??e mieli??my ju?? napisany prosty skrypt pythona do wysy??ania zapyta?? do bazy i tym samym session id by??o w nim parametrem.
Cookie zawiera??o pewien numer oraz user ID, co jest do???? dziwne.
Uznali??my wi??c, ??e mo??e da si?? sfabrykowa?? cookie admina.
W bazie danych w tabeli u??ytkownik??w znajdowa??o si?? dziwne pole `last login timestamp`.
Znaczniki czasowe cz??sto s?? stosowane jako ziarna dla randoma, wi??c sprawdzili??my co da nam random dla naszego timestampa jako ziarna i otrzymali??my liczb?? z naszego cookie!

W zwi??zku z tym wyci??gn??li??my z bazy timestamp dla admina przez SQL Injection, ustawili??my ziarno randoma na t?? warto????, pobrali??my losow?? liczb??, po????czyli??my z ID admina i uzyskali??my cookie `1229569179-209`, kt??re pozwoli??o zalogowa?? si?? do aplikacji jako admin i uzyska?? flag??.
