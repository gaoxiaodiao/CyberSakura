## Secu Prim (PPC, 65p)

###ENG
[PL](#pl-version)

After connecting to the server we get a PoW to solve, and then the task is to provide number of primes and perfect powers in given range.

The ranges are rather small (less than 2000 numbers in between) so we simply iterate over the given range and use `gmpy` to tell us if the number if a probable prime or a perfect power:

```python
def solve_task(start, end):
    print("Range size = " + str(end - start))
    counter = 0
    for i in range(start, end + 1):
        if gmpy2.is_prime(i):
            counter += 1
        elif gmpy2.is_power(i):
            counter += 1
    print("Counted " + str(counter))
    return counter
```

And the whole script with PoW:

```python
import hashlib
import re
import socket

import itertools
import string
import gmpy2


def recvuntil(s, tails):
    data = ""
    while True:
        for tail in tails:
            if tail in data:
                return data
        data += s.recv(1)


def proof_of_work(s):
    data = recvuntil(s, ["Enter X:"])
    x_suffix, hash_prefix = re.findall("X \+ \"(.*)\"\)\.hexdigest\(\) = \"(.*)\.\.\.\"", data)[0]
    len = int(re.findall("\|X\| = (.*)", data)[0])
    print(data)
    print(x_suffix, hash_prefix, len)
    for x in itertools.product(string.ascii_letters + string.digits, repeat=len):
        c = "".join(list(x))
        h = hashlib.sha256(c + x_suffix).hexdigest()
        if h.startswith(hash_prefix):
            return c


def get_task(s):
    sentence = recvuntil(s, ["that: "])
    sentence += recvuntil(s, ["\n"])
    return sentence


def solve_task(start, end):
    print("Range size = " + str(end - start))
    counter = 0
    for i in range(start, end + 1):
        if gmpy2.is_prime(i):
            counter += 1
        elif gmpy2.is_power(i):
            counter += 1
    print("Counted " + str(counter))
    return counter


def main():
    url = "secuprim.asis-ctf.ir"
    port = 42738
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    x = proof_of_work(s)
    print(x)
    s.sendall(x + "\n")
    data = recvuntil(s, "---\n")
    print(data)
    while True:
        data = recvuntil(s, ["like n such", "corret!", "}"])
        print(data)
        if "ASIS" in data:
            print(data)
        if "corret" in data:
            print("failed")
            break
        else:
            task = get_task(s)
            print(task)
            b, e = re.findall("that: (\d+) <= n <= (\d+)", task)[0]
            start = int(b)
            end = int(e)
            counter = solve_task(start, end)
            s.sendall(str(counter) + "\n")


main()
```

###PL version

Po po????czeniu do serwera dostajemy PoW do rozwi??zania a nast??pnie zadaniem jest policzy?? ile liczb pierwszych oraz doskona??ych pot??g jest w zadanym przedziale.

Przedzia??y s?? do???? ma??e (nie wi??cej ni?? 2000 liczb) wi??c po prostu iterujemy po ka??dej liczbie i za pomoc?? `gmpy` sprawdzamy czy liczba jest pierwsza lub czy jest doskona???? pot??g??:

```python
def solve_task(start, end):
    print("Range size = " + str(end - start))
    counter = 0
    for i in range(start, end + 1):
        if gmpy2.is_prime(i):
            counter += 1
        elif gmpy2.is_power(i):
            counter += 1
    print("Counted " + str(counter))
    return counter
```

A ca??y skrypt razem z PoW:

```python
import hashlib
import re
import socket

import itertools
import string
import gmpy2


def recvuntil(s, tails):
    data = ""
    while True:
        for tail in tails:
            if tail in data:
                return data
        data += s.recv(1)


def proof_of_work(s):
    data = recvuntil(s, ["Enter X:"])
    x_suffix, hash_prefix = re.findall("X \+ \"(.*)\"\)\.hexdigest\(\) = \"(.*)\.\.\.\"", data)[0]
    len = int(re.findall("\|X\| = (.*)", data)[0])
    print(data)
    print(x_suffix, hash_prefix, len)
    for x in itertools.product(string.ascii_letters + string.digits, repeat=len):
        c = "".join(list(x))
        h = hashlib.sha256(c + x_suffix).hexdigest()
        if h.startswith(hash_prefix):
            return c


def get_task(s):
    sentence = recvuntil(s, ["that: "])
    sentence += recvuntil(s, ["\n"])
    return sentence


def solve_task(start, end):
    print("Range size = " + str(end - start))
    counter = 0
    for i in range(start, end + 1):
        if gmpy2.is_prime(i):
            counter += 1
        elif gmpy2.is_power(i):
            counter += 1
    print("Counted " + str(counter))
    return counter


def main():
    url = "secuprim.asis-ctf.ir"
    port = 42738
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    x = proof_of_work(s)
    print(x)
    s.sendall(x + "\n")
    data = recvuntil(s, "---\n")
    print(data)
    while True:
        data = recvuntil(s, ["like n such", "corret!", "}"])
        print(data)
        if "ASIS" in data:
            print(data)
        if "corret" in data:
            print("failed")
            break
        else:
            task = get_task(s)
            print(task)
            b, e = re.findall("that: (\d+) <= n <= (\d+)", task)[0]
            start = int(b)
            end = int(e)
            counter = solve_task(start, end)
            s.sendall(str(counter) + "\n")


main()
```
