# Multicast (misc, 175p)

## ENG
[PL](#pl-version)

In the task we get a [sage script](generate.sage) which generated the [data](data.txt):

```python
nbits = 1024
e = 5
flag = open("flag.txt").read().strip()
assert len(flag) <= 64
m = Integer(int(flag.encode('hex'),16))
out = open("data.txt","w")

for i in range(e):
    while True:    
        p = random_prime(2^floor(nbits/2)-1, lbound=2^floor(nbits/2-1), proof=False)
        q = random_prime(2^floor(nbits/2)-1, lbound=2^floor(nbits/2-1), proof=False)
        ni = p*q
        phi = (p-1)*(q-1)
        if gcd(phi, e) == 1:
            break

    while True:
        ai = randint(1,ni-1)
        if gcd(ai, ni) == 1:
            break

    bi = randint(1,ni-1)
    mi = ai*m + bi
    ci = pow(mi, e, ni)
    out.write(str(ai)+'\n')
    out.write(str(bi)+'\n')
    out.write(str(ci)+'\n')
    out.write(str(ni)+'\n')
```

It is a standard RSA with e=5 and 1024 bits modulus.
What is noticable is that we get 5 payloads, and e is 5, so the setup looks very much like for a Hastad Broadcast Attack.
Also the name of the task could suggest this.

However, unlike for the simple Hastad case, we don't really have the same message sent with different moduli.
Such case can be solved very simply using Chinese Reminder Theorem.
Here each of the encrypted messages is different, however each has form `ai*m + bi` so a linear polynomial was applied over the message before the encryption.

If we look at the generic Hastad description, for example in Durfee PhD Thesis http://theory.stanford.edu/~gdurf/durfee-thesis-phd.pdf (page 25-26) we will find that in fact it is also applicable in out scenario, although the final coputation requires Coppersmith attack.

We follow the method described in the linked paper (for details just read the paper) and we get a [solver](solver.sage) with the core part:

```python
def main():
	import codecs
   	with codecs.open("data.txt", "r") as input_file:
		data = [int(c) for c in input_file.readlines()]
		a = [data[i * 4] for i in range(5)]
		b = [data[i * 4+1] for i in range(5)]
		c = [data[i * 4+2] for i in range(5)]
		ns = [data[i * 4 + 3] for i in range(5)]
		t = []
		for n in ns:
			other_moduli = [x for x in ns if x != n]
			t.append(crt([1,0,0,0,0],[n]+other_moduli))
		N = reduce(lambda x,y: x*y, ns)
		e = 5
		P.<x> = PolynomialRing(Zmod(N), implementation='NTL');
		pol = 0
		for i in range(5):
			pol += t[i]*((a[i]*x+b[i])^e - c[i])
		dd = pol.degree()
		if not pol.is_monic():
			leading = pol.coefficients(sparse=False)[-1]
			inverse = inverse_mod(int(leading), int(N))
			pol *= inverse
		beta = 1
		epsilon = beta / 7
		mm = ceil(beta**2 / (dd * epsilon))
		tt = floor(dd * mm * ((1/beta) - 1))
		XX = ceil(N**((beta**2/dd) - epsilon))
		roots = pol.small_roots()
		for root in roots:
			print(long_to_bytes(root))
	
main()
```

So we read the data and partition them into the recovered polynomials coefficients and moduli.
We use Chinese Reminder Theorem to get values `ti` which for each dataset `i` should give 1 mod `ni` and 0 modulo any other of the moduli.
Then we calculate the product of all moduli and create a polynomial ring with this value, because now all calculations will be mod `n1*n2*...`.

Finally we create a polynomial suggested by Durfee and we find the roots using Coppersmith method.

The extracted root is the message we were looking for: `PCTF{L1ne4r_P4dd1ng_w0nt_s4ve_Y0u_fr0m_H4s7ad!}`


## PL version

W zadaniu dostajemy [skrypt sage](generate.sage) kt??ry wygenerowa?? [dane](data.txt):

```python
nbits = 1024
e = 5
flag = open("flag.txt").read().strip()
assert len(flag) <= 64
m = Integer(int(flag.encode('hex'),16))
out = open("data.txt","w")

for i in range(e):
    while True:    
        p = random_prime(2^floor(nbits/2)-1, lbound=2^floor(nbits/2-1), proof=False)
        q = random_prime(2^floor(nbits/2)-1, lbound=2^floor(nbits/2-1), proof=False)
        ni = p*q
        phi = (p-1)*(q-1)
        if gcd(phi, e) == 1:
            break

    while True:
        ai = randint(1,ni-1)
        if gcd(ai, ni) == 1:
            break

    bi = randint(1,ni-1)
    mi = ai*m + bi
    ci = pow(mi, e, ni)
    out.write(str(ai)+'\n')
    out.write(str(bi)+'\n')
    out.write(str(ci)+'\n')
    out.write(str(ni)+'\n')
```

Mamy tu standardowe RSA e=5 oraz 1024 bitowym modulusem.
Mo??emy zauwa??y??, ??e mamy 5 wiadomo??ci oraz e r??wne 5, co sugeruje konfiguracje podobn?? do ataku Hastad Broadcast.
Dodatkowo sama nazwa zadania tak??e mo??e to sugerowa??.

Jednak, w przeciwie??stwie do klasycznego przypadku Hastada, nie mamy tutaj tej samej wiadomo??ci wys??anej z r????nymi modulusami.
Taki przypadek trywialnie mo??na rozwi??za?? za pomoc?? Chi??skiego Twierdzenia o Resztach.
Tutaj ka??da wiadomo???? jest inna, niemniej jednak ka??da ma posta?? `ai*m + bi` wi??c pewien liniowy wielomian zosta?? policzony z wiadomo??ci przed szyfrowaniem.

Je??li popatrzymy na og??lny przypadek Hastada, na przyk??ad w pracy doktorskiej pana Durfee http://theory.stanford.edu/~gdurf/durfee-thesis-phd.pdf (strony 25-26) zobaczymy, ??e w rzeczywisto??ci twierdzenie mo??na wykorzysta?? tak??e w naszym przypadku, chocia?? finalne obliczenia b??d?? wymaga?? u??ycia ataku Coppersmitha.

Post??pujemy zgodnie z metod?? opisan?? w linkowanej publikacji (po szczeg????y i wyja??nienia odsy??am tam) i dostajemy [solver](solver.sage) z g????wn?? cz????ci??:

```python
def main():
	import codecs
   	with codecs.open("data.txt", "r") as input_file:
		data = [int(c) for c in input_file.readlines()]
		a = [data[i * 4] for i in range(5)]
		b = [data[i * 4+1] for i in range(5)]
		c = [data[i * 4+2] for i in range(5)]
		ns = [data[i * 4 + 3] for i in range(5)]
		t = []
		for n in ns:
			other_moduli = [x for x in ns if x != n]
			t.append(crt([1,0,0,0,0],[n]+other_moduli))
		N = reduce(lambda x,y: x*y, ns)
		e = 5
		P.<x> = PolynomialRing(Zmod(N), implementation='NTL');
		pol = 0
		for i in range(5):
			pol += t[i]*((a[i]*x+b[i])^e - c[i])
		dd = pol.degree()
		if not pol.is_monic():
			leading = pol.coefficients(sparse=False)[-1]
			inverse = inverse_mod(int(leading), int(N))
			pol *= inverse
		beta = 1
		epsilon = beta / 7
		mm = ceil(beta**2 / (dd * epsilon))
		tt = floor(dd * mm * ((1/beta) - 1))
		XX = ceil(N**((beta**2/dd) - epsilon))
		roots = pol.small_roots()
		for root in roots:
			print(long_to_bytes(root))
	
main()
```

Pobieramy dane i dzielimy je na odpowiednie parametry wielomian??w i modulusy.
Nast??pnie za pomoc?? Chi??skiego Twierdzenia o Resztach wyliczamy wsp????czynniki `ti` kt??re dla ka??dego wej??cia `i` daj?? 1 mod `ni` oraz 0 modulo dowolny inny modulus z zestawu.
Nast??pnie wyliczamy iloczyn wszystkich modulus??w i tworzymy pier??cie?? wielomianowy z tym iloczynem, poniewa?? wszystkie obliczenia wykonywane b??d?? teraz modulo `n1*n2*...`.

Finalnie tworzymy wielomian zaproponowany przez Durfee i znajdujemy jego pierwiastki metod?? Coppersmitha.

Znaleziony pierwiastek to szukana flaga: `PCTF{L1ne4r_P4dd1ng_w0nt_s4ve_Y0u_fr0m_H4s7ad!}`
