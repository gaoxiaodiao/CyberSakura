# SMTPresident (crypto 400)


###ENG
[PL](#pl-version)

This was sadly a very badly designed task, because the last step was broken and required a crystal ball to figure out what auther had in mind.
Unfortunately we figured this out after the CTF was over.

In this task we get 170 encrypted emails, 170 public keys for them and encrypted flag.
First thing we notice is that there are 17 emails per single date.
Next we notice that each pubblic key has public exponent `e` equal to 17.

This automatically bring to mind the Hastad broadcast attack using Chinese Reminder Theorem!
We assume here that each day the message that was sent is identical and therefore we have CRT resiude-modulus pairs.

We solve CRT with:

```python
def solve_crt(residues, moduluses):
    import gmpy2
    N = reduce(lambda x, y: x * y, moduluses)
    Nxs = [N / n for n in moduluses]
    ds = [gmpy2.invert(N / n, n) for n in moduluses]
    mults = [residues[i] * Nxs[i] * ds[i] for i in range(len(moduluses))]
    return reduce(lambda x, y: x + y, mults) % N
```

This way we hopefully get `message ^ 17` and by applying integer nth root we recover the value of `message` for each date.
Messages are for example:

```
4/5/16
Sub##ct:#My ##llow#D#C#Mem###s
#onte#t:##e#p t#####a## <MI#SIN##1#62866###4###8349#477####17117####0#97909##6#6##248#11##0478#######87##3##0169#2######30#71###### th#######e#key #####r### o#.
4/2/16
####e#t:##y F#l#o# DN# #e###r#
Co#ten## Kee# this#s##e #M#S#I##>18#2#661##4##08#4##47#2#1#1##1#5#6#0#9#90###6467#24##1180###8#2#29##8705350##6#####6#13#0#7###553# t##t'# ##e key #e a#ree####.
```
So it seems it's a single message just with missing bytes in different mails.
We combine this to get:

```
Subject: My Fellow DNC Members
Content: Keep this safe <MISSING>1862866103431083493477241717117566609979097064670248011800478128293487053500169824960133057115553, that's the key we agreed on.
```

And now comes the uber-confusing guessing part.
Apparently author assumed that we will figure out that he meant the number above does not only specify the suffix of the decryption exponent but also the low bits.
This of course is not justified at all by the data we have, it's just a pure guess.
But it you follow this, you can recover most of `d` bits simply by checking which combination of higher bits won't change the suffix value.

In the end you can run a standard partial key recovery algorithm and even with high public exponent 65537 you can recover the key reasonably quickly.

This could, theoretically, be solved without a crystal ball, but it would require significant computational power...

###PL version

To niestety by??o bardzo ??le zaprojektowane zadanie, g????wnie dlatego, ??e ostatni krok wymaga?? szklanej kuli, ??eby zgadna?? co autor mia?? na my??li.
Nam uda??o sie to dopiero po zako??czeniu CTFa.

W tym zadaniu dostajemy na pocz??tku 170 zaszyfrowanych maili, 170 kluczy publicznych oraz zaszyfrowan?? flag??.
Pierwsza rzecz kt??r?? zauwa??amy, to fakt, ??e ka??dego dnia jest 17 maili.
Nast??pnie zauwa??amy, ??e publiczny wyk??adnik szyfrujacy wynosi 17.

To automatycznie przywodzi na my??l atak Hastad broadcast z wykorzystaniem Chi??skiego Twierdzenia o Resztach.
Zak??adamy tutaj, ??e ka??dego dnia wysy??ano t?? sam?? wiadomo???? a tym samym znamy pary reszta-modulus dla CRT.

Rozwi??zujemy CRT:

```python
def solve_crt(residues, moduluses):
    import gmpy2
    N = reduce(lambda x, y: x * y, moduluses)
    Nxs = [N / n for n in moduluses]
    ds = [gmpy2.invert(N / n, n) for n in moduluses]
    mults = [residues[i] * Nxs[i] * ds[i] for i in range(len(moduluses))]
    return reduce(lambda x, y: x + y, mults) % N
```

I w ten spos??b liczymy na otrzymanie warto??ci `message^17` i wyliczaj??c ca??kowity pierwiastek 17 stopnia odzyskujemy warto???? `message` dla ka??dej daty.
Wiadomo??ci kt??re dostajemy wygl??daj?? tak:

```
4/5/16
Sub##ct:#My ##llow#D#C#Mem###s
#onte#t:##e#p t#####a## <MI#SIN##1#62866###4###8349#477####17117####0#97909##6#6##248#11##0478#######87##3##0169#2######30#71###### th#######e#key #####r### o#.
4/2/16
####e#t:##y F#l#o# DN# #e###r#
Co#ten## Kee# this#s##e #M#S#I##>18#2#661##4##08#4##47#2#1#1##1#5#6#0#9#90###6467#24##1180###8#2#29##8705350##6#####6#13#0#7###553# t##t'# ##e key #e a#ree####.
```

Wi??c wida??, ??e to jedna wiadomo????, tylko dla r????nych dat brakuje r????nych fragment??w.
Sk??adamy to i dostajemy:

```
Subject: My Fellow DNC Members
Content: Keep this safe <MISSING>1862866103431083493477241717117566609979097064670248011800478128293487053500169824960133057115553, that's the key we agreed on.
```

I teraz nast??puje bardzo dziwna cz?????? zgaduj zgaduli.
Najwyra??niej autor za??o??y??, ??e wpadniemy na to, ??e liczba powy??ej nie okre??la jedynie suffixu wyk??adnika deszyfruj??cego, ale tak??e niskie bity.
To jest oczywi??cie niczym nie poparte w danych kt??rymi dysponujemy, to zwyk??e zgadywanie.
Ale je??li poczynimy takie za??o??enie, mo??emy odzyska?? wi??kszo???? bit??w `s` zwyczajnie testuj??c kt??re kombinacje wysokich bit??w nie zmieni?? nam suffixu.

Finalnie mo??emy uruchomi?? standardowy algorytm odzyskiwania klucza z cz????ciowych danch i nawet dla wysokiej eksponenty 65537 mo??emy odzyska?? klucz wzlg??dnie szybko.

To teoretycznie mo??na by te?? rozwi??za?? bez szklanej kuli, ale wymaga??oby do???? sporej mocy obliczeniowej...
