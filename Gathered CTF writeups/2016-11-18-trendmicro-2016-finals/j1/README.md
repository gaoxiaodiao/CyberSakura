# J1 (forensics)

###ENG
[PL](#pl-version)

This was a multilevel forensics task.

We were given a windows virtual machine to work with. 
The machine had user "M" with unknown password.
Intially we reset the password, but this turned out to be a bad idea since the user had bitlocker encrypoted files and the password was necessary after all.
So we used Ophcrack to recover the password hash `f6939966b0ffbc61c2c520cea20c2db0` and some online breaker told us this is `qwerty1234`.

Now we could decrypt the files:

* A picture with some meaningless email
* Email hinting that admin likes to use the same password in many places
* html page with some javascript

The javascript has some placeholders for parameters we had to guess/bruteforce but after a while we got:

```javascript
for (var d = 11; d < 12; d++) {
	var key = "";
	var clear = "";
	var encrypted = "96.28.95.118.9.2.58.29.56.52.44.25.58.51.83.8.108.20.53.37.88.2.71.80";
	secret = navigator.platform + "en-UStrue2000" ;

	for (i=0; i < secret.length; i++) { key+= String.fromCharCode(secret.charCodeAt(i) ^ d);}
	encrypted = encrypted.split ("."); for (i=0; encrypted.length > key.length; i++) { key += key; }

	for (i=0; i < encrypted.length; i++) { clear += String.fromCharCode(key.charCodeAt(i) ^ parseInt(encrypted[i]));}
	document.write (clear + "<br>");
}
```

and were left with the only interesting result:

```
<~:N0l_;flS`D]j3W/iG=:~>
```

It took us a while to realise that this is ASCII85 encoding and it decodes to `OpenStego v0.6.1`.

We used this tool on the picture we recovered, using the same admin password (as hinted in the recovered email) and we got a doc file from this.

This doc file contained a macro with flag decryption.
Sadly none of us had MS Word to open this :( Luckily quick thinking of one of our players saved us.
He uploaded this Word file to Malwr, which then opened the file inside a sandbox and provided us with a useful memory dump.
Among other things there was a base64 string, which decoded finally gave us the flag.


###PL version

Zadanie by??o wielopoziomowym problemem z informatyki ??ledczej.

Dostali??my windowsow?? maszyn?? wirtualn?? do pracy.
Na maszynie by?? u??ytkownik "M" z nieznanym has??em.
Pocz??tkowo zresetowali??my has??o, ale to okaza??o si?? z??ym pomys??em, bo na dysku by??y pliku szyfrowane bitlockerem i has??o by??o potrzebne ??eby je odzyska??.
U??yli??my Ophcracka ??eby odzyska?? hash has??a `f6939966b0ffbc61c2c520cea20c2db0` a jaki?? onlinowy hash breaker powiedzia?? ??e to `qwerty1234`.

Teraz mogli??my odszyfrowa?? pliki:

* Obrazek z nieistotnym mailem
* Mail wspominaj??cy ??e admin lubi u??ywa?? tego samego has??a wielokrotnie
* Stron?? html ze skryptem JS

Skrypt mia?? pewne placeholdery kt??re trzeba by??o zgadn???? / brutowa?? ale po pewnym czasie uzyskali??my:

```javascript
for (var d = 11; d < 12; d++) {
	var key = "";
	var clear = "";
	var encrypted = "96.28.95.118.9.2.58.29.56.52.44.25.58.51.83.8.108.20.53.37.88.2.71.80";
	secret = navigator.platform + "en-UStrue2000" ;

	for (i=0; i < secret.length; i++) { key+= String.fromCharCode(secret.charCodeAt(i) ^ d);}
	encrypted = encrypted.split ("."); for (i=0; encrypted.length > key.length; i++) { key += key; }

	for (i=0; i < encrypted.length; i++) { clear += String.fromCharCode(key.charCodeAt(i) ^ parseInt(encrypted[i]));}
	document.write (clear + "<br>");
}
```

i otrzymali??my jedyny sensowny wynik:

```
<~:N0l_;flS`D]j3W/iG=:~>
```

Chwile zaj????o nam odkrycie ??e to string kodowany jako ASCII85 i dekoduje si?? do `OpenStego v0.6.1`.

U??yli??my tego narz??dzia na odzyskanym obrazku, u??ywaj??c tego samego has??a admina (jak zasugerowano w mailu kt??ry odzyskali??my) i dostali??my z tego plik doc.

Ten plik worda zawiera?? makro kt??re dekodowa??o flag??.
Niestety nikt z nas nie mia?? pod r??k?? MS Worda i nie mogli??my tego otworzy??.
Szcz????liwie uratowa?? nas ??wietny pomys?? jednego z graczy.
Wrzuci?? on rzeczony plik na Malwr, gdzie plik zosta?? otwarty w sandboxie, z kt??rego dostali??my u??yteczny memdump.
Po??r??d r????nych rzeczy by?? tam string base64, kt??ry po zdekodowaniu da?? nam flag??.
