# Chinese Satellite (crypto 200)


## ENG
[PL](#pl-version)

This task was very strange.
The author clearily didn't understand quantum key exchange at all, and in this particular case knowing how this should work was making the task harder to solve...

In the task we get some intercepted quantum transfers [sat->ground](q_transmission_1), [ground->sat](q_transmission_2), [sat->ground](q_transmission_3) and a ciphertext in public channel:

`269118188444e7af980a245aedce5fb2811b560ccfc5db8e41f102a23f8d595ffde84cb1b3f7af8efd7a919bd2a7e6d3`

In general quantum key exchange is quite simple:

1. Alice sends set of random bits encoded in one of two bases (let's call them X and Y)
2. Bob receives the qbits and randomly selects which base to use to measure value (since he can't know which base Alice used for each of qbits). Statistically he will get about half of the bases right.
3. Bob sends to Alice information which bases he used for each of the qbits.
4. Alice compares the list from Bob with the bases she actually used and sends to Bob information which bases he got right.

In case Bob used the right base he knows the bit value Alice wanted to send.
Those agreed bits are then normally used as some symmetric key for the communication.

We have our 3 transmissions, and they are exactly what described above: 

1. First one is the whole dump of initial qbits sent by Alice. We have two bases -> straight (`-` or `|`) and cross (`/` or `\`).
2. Second one is bases Bob used - straight `+` or cross `x`.
3. Last one is the list of bits Bob got right marked as `v`.

So we can simply read values sent by Alice in 1st transmission for which there is `v` in last tramissions and we will get the qbits that they got right. We don't really know if `\` is 0 or 1 and if `|` is 0 or 1, but this is simple enough, we can just test all 4 options.

```python
def get_agreed_bytes(data_sent, bases_measured, bases_correct, v1, v2):
    agreed_bits = []
    for i in range(len(bases_correct)):
        if bases_correct[i] == 'v':
            if bases_measured[i] == '+':
                if data_sent[i] == '-':
                    agreed_bits.append(v1)
                else:
                    agreed_bits.append(abs(v1 - 1))
            else:
                if data_sent[i] == '/':
                    agreed_bits.append(v2)
                else:
                    agreed_bits.append((abs(v2 - 1)))
    return hex(int("".join([str(c) for c in agreed_bits]), 2))[2:-1]
```

Now it was strange, because we get some bits and we don't know how to use them as encryption key to recover the flag.
Fortunately we noticed that byte values seem in printable range and I printed out the agreed bytes and one of the options was:

`iv:281e6bfc14a9aad39845f29b30ef1334,key:b340fe5025b06657034822b340ceb9d4,algo:aes_cbc`

Which makes little sens in terms of crypto channel key exchange, because Alice can't know which bits Bob will get, but whatever...

So we have all we need -> algo and parameters and we can just decrypt the flag: `h4ck1t{tr4nsmi55i0n_0v3r_bb84_l00ks_s3cur3_0k}`

Complete solver [here](quantum.py)

## PL version

To by??o do???? dziwne zadanie.
Autor ewidentnie nie rozumie o co chodzi w kwantowej wymianie klucza i paradoksalnie w tym zadaniu znajomo???? tego zagadnienia tylko utrudnia??a rozwi??zanie zadania...

W zadaniu dostajemy kilka przechwyconych kwantowych transmisji [sat->ground](q_transmission_1), [ground->sat](q_transmission_2), [sat->ground](q_transmission_3) i szyfrogram w publicznym kanale:

`269118188444e7af980a245aedce5fb2811b560ccfc5db8e41f102a23f8d595ffde84cb1b3f7af8efd7a919bd2a7e6d3`

Generalnie kwantowa wymiana klucza jest do???? prosta:

1. Alice wysy??a do Boba losowe bity kodowane w jednej z dw??ch baz (nazwijmy je X i Y)
2. Bob odbiera qbity i wybiera losowo w jakiej bazie odczyta?? warto???? (poniewa?? nie wie w jakiej bazie warto???? zosta??a zakodowana przez Alice). Statystycznie powinien odczyta?? oko??o po??owy poprawnie.
3. Bob wysy??a do Alice informacje kt??rych baz u??y?? dla ka??dego z qbit??w.
4. Alice por??wnuje list?? od Boba ze swoj?? list?? z bazami kt??rych u??y??a i wysy??a do Boba informacje, kt??re bazy wybra?? poprawnie.

Je??li Bob u??y?? dobrej bazy dla danego bitu to zna warto???? kt??r?? Alice chcia??a wys??a??.
Bity, kt??re si?? zgodzi??y s?? zwykle u??ywane do generacji klucza dla kryptografii symetrycznej.

Mamy 3 tranmisje danych i s?? dok??adnie tym co opisane wy??ej:

1. Pierwsza to zrzut qit??w kt??re Alice wys??a??a. Mamy tam dwie bazy -> prost?? (`-` i `|`) oraz sko??n?? (`/` i `\`).
2. Druga to lista baz kt??rych u??y?? Bob - prosta `+` lub sko??na `x`.
3. Ostatnia to lista bit??w kt??re Bob odczyta?? dobrze, oznaczonych przez `v`.

Mo??emy wi??c po prostu odczyta?? warto??ci kt??re Alice wys??a??a w 1 transmisji, dla kt??rych w trzeciej transmisji mamy `v` i w ten spos??b poznamy list?? qbit??w kt??re si?? zgodzi??y.
Nie wiemy co prawda czy `\` to 1 czy 0 oraz czy `|` to 1 czy 0, ale mo??emy przetestowa?? wszystkie 4 opcje.

```python
def get_agreed_bytes(data_sent, bases_measured, bases_correct, v1, v2):
    agreed_bits = []
    for i in range(len(bases_correct)):
        if bases_correct[i] == 'v':
            if bases_measured[i] == '+':
                if data_sent[i] == '-':
                    agreed_bits.append(v1)
                else:
                    agreed_bits.append(abs(v1 - 1))
            else:
                if data_sent[i] == '/':
                    agreed_bits.append(v2)
                else:
                    agreed_bits.append((abs(v2 - 1)))
    return hex(int("".join([str(c) for c in agreed_bits]), 2))[2:-1]
```

Teraz nast??puje do???? dziwny krok, bo mamy zgodne bity, ale nie wiemy co dalej z nimi zrobi?? ??eby odzyska?? flag??.
Szcz????lwie zauwa??yli??my, ??e warto??ci bajt??w wygl??daj?? na drukowalne ascii wi??c wypisali??my sobie uzyskane mo??liwo??ci i dostali??my dla jednego z nich:

`iv:281e6bfc14a9aad39845f29b30ef1334,key:b340fe5025b06657034822b340ceb9d4,algo:aes_cbc`

Co zupe??nie nie ma sensu z punktu widzenia kwantowej wymiany klucza, bo Alice nie mog??a wiedzie?? kt??re bity Bob odzyta poprawnie, no ale co tam...

Mamy podany algorytm i prametry wi??c odszyfrowujemy flag??: `h4ck1t{tr4nsmi55i0n_0v3r_bb84_l00ks_s3cur3_0k}`

Ca??y solver [tutaj](quantum.py)
