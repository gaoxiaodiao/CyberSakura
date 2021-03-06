# V1rus3pidem1c (web 100)

## ENG
[PL](#pl-version)

In the task we get a webpage where we can select a country from dropdown and for some countries this shows us file upload form and for some of them it doesn't.
For example there is a form for `Germany` and no form for `Russia`.

The country name is passed as GET parameter in the query, and we decide to see what exactly is done with it.
A little bit of fuzzing tells us that it goes into some SQL query into where condition.

With classic `country=Russia' or '1'='1` we get a form for Germany, which means we managed to exploit the task with SQL Injection.

We tried a bit to get some echo here, but couldn't, so we simply switched to run Blind SQLi attack.
We got a simple oracle function:

```
import requests
session = requests.session()

def is_true(condition):
    url = "http://tasks.ctf.com.ua:13372/index.php?country=Russia' or (%s) -- a" % condition
    result = session.get(url)
    return 'virus for Germany' in result.text


def main():
    print(is_true("1=1"))
    print(is_true("1=0"))


main()
```

And with this we can extract `Information_Schema.Tables` and `Information_Schema.Columns` data, with simple substring and byte-by-byte comparison using the oracle function.

This tells us there we have only a single user defined table and it contains only `countryID, countryName, scriptPath`.
Last parameter is especially interesting since it's an actual path to php script with form, which gets included on the page.
It's in form: `country/ge.php`, `country/tu.php` etc.

We could use our SQLi to include some other file by `index.php?country=' union select 'somefile.php' -- comment`, but we can't put any file on the server.
But since we control the include path we decided to check good old php wrappers and force the server to include: `php://filter/read=convert.base64-encode/resource=country/ge.php` and as expected we get a nice base64 contents of the php script.

It seems that the files uploaded by the form available for some countries actually get uploaded to the server!
We have there for example:

```php
<?php

	$target_dir = "uploads/";
	$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
	move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file);
	
	/*echo $_FILES["fileToUpload"]["tmp_name"] ."\n";
	var_dump($_FILES["fileToUpload"]);
	var_dump(file_exists($_FILES["fileToUpload"]["tmp_name"]));
	echo file_exists($target_file);*/
?>
```

So it's clear that we can use this form to upload a php shell to the server and then use SQLi to include it on the page and execute, because we know the file will be under `uploads/file_name`.

We proceed with this and find a hidden php file with flag: `h4ck1t{$QL&LFI=FR13ND$}`

## PL version

W zadaniu dostajemy link do strony internetowej gdzie mo??emy wybra?? z listy jeden z kraj??w i dla niekt??rych pojawia si?? formularz uploadu plik??w a dla innych nie.

Na przyk??ad dla `Germany` mamy formularz a dla `Russia` nie.

Nazwa kraju jest przesy??ana jako parametr GET i spr??bowali??my przetestowa?? co si?? mo??e dzia?? z tym parametrem.
Troche fuzzowania pokaza??o ??e parametr idzie bezpo??rednio do query SQL do warunku where.

Klasycznym `country=Russia' or '1'='1` dostali??my formular dla Niemiec, co znaczy ??e mamy tam SQL Injection.

Pr??bowalismy dosta?? tam gdzie?? echo, ale bez skutku, wi??c postanowili??my u??y?? Blind SQLi.
Przygotowalismy prost?? funkcje:

```
import requests
session = requests.session()

def is_true(condition):
    url = "http://tasks.ctf.com.ua:13372/index.php?country=Russia' or (%s) -- a" % condition
    result = session.get(url)
    return 'virus for Germany' in result.text


def main():
    print(is_true("1=1"))
    print(is_true("1=0"))


main()
```

I mo??emy dzi??ki temu pobra?? z `Information_Schema.Tables` i `Information_Schema.Columns` dane poprzez proste substring oraz por??wnywanie warto??ci bajt po bajcie za pomoc?? funkcji oracle.

St??d wiemy, ??e jest tylko jedna tabela u??ytkownika i zawiera `countryID, countryName, scriptPath`.

Ostatni parametr jest szczeg??lnie ciekawy bo zawiera ??cie??k?? do plik??w php, kt??re s?? includowane na stronie.

Maj?? posta??: `country/ge.php`, `country/tu.php` etc.

Mogliby??my u??y?? naszego SQLi ??eby includowa?? jaki?? inny plik przez `index.php?country=' union select 'somefile.php' -- comment` ale nie mo??emy p??ki co umie??ci?? niczego na serwerze.

Niemniej skoro kontrolujemy ??cie??k?? do include to mo??e stare dobre wrappery php zadzia??aj?? i czy serwer pozwoli includowa??: `php://filter/read=convert.base64-encode/resource=country/ge.php` i tak jak na to liczylismy, dostali??my ??adne base64 z kodu skryptu.

Analiza kodu pozwala stwierdzi??, ??e mo??emy uploadowa?? pliki na serwer za pomoc?? skrypt??w dla niekt??rych kraj??w!
Mamy tam:

```php
<?php

	$target_dir = "uploads/";
	$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
	move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file);
	
	/*echo $_FILES["fileToUpload"]["tmp_name"] ."\n";
	var_dump($_FILES["fileToUpload"]);
	var_dump(file_exists($_FILES["fileToUpload"]["tmp_name"]));
	echo file_exists($target_file);*/
?>
```

Wida?? wyra??nie, ??e mozemy spokojnie wrzuci?? za pomoc?? formularza shell php na serwer i u??y?? SQLi ??eby go includowa?? i u??y??, bo wiemy ??e jest dost??pny pod `uploads/file_name`.

Umieszczamy wi??c nasz shell i odnajdujemy ukryty plik php z flag??: `h4ck1t{$QL&LFI=FR13ND$}`
