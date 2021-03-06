# DES (Crypto 500)

###ENG
[PL](#pl-version)

The general idea was simple -  the authors used double encryption with DES and Blowfish and the task was to decode the message.

The problems:

* Authors used some shady website for encryption and not the ciphers directly. This website was adding random paddings and without knowing about it, there was no way to solve it. Fortunately this was released as a hint.
* The authors for no apparent reason have given an example payload apart from the flag. This suggested a meet-in-the-middle attack using this payload, which was not a good approach, because the example payload was encrypted with different keys than the flag.
* The calculations for this task were a bit time consuming due to key universum size. Seriously, there is no need to make a task where bruteforce is taking minutes to run on 8 paralell cores. It doesn't make the task any "harder", only more annoying.

So what we have here is the encrypted flag:

```
AiEjLYxiRUlgG+OYaYje5HOwvS8UFegdXRrCsIiy6pBH67fDvGbLF/gtZihyW7WYVOrsi7/N1sgaVUBU/VW1NwEOrOhguZZfP5T7Gw88sMx9KFepLfsjOLPKKVUuMbVu6Lno0FJjbU+7ft1VtdsQhAh1Lc91SDcduoI3J1FwffwwEwy1L7FKjg14LZ9fgaMF5c43T8avL+bpOBDFHiPzK1Mwv4ftVt6k5UV13cPV3VLm+Jx7Q/7LLamyQLLUU0O1pcKZOHi7oYPngpFh7VmIPIJwCsmoCAyt8+yC/uqNgpfUoD0SHfG7tvz7F8sZKL6RfezLvFN++8B+rs+6AGOiSHCmnGbO4PNcOdZfWP4lYZQRIZ/DTN4ntg==
```

And we know that the flag was encrypted first with DES with padding, the data were transformed into base64 and this was encrypted again with Blowfish with padding and it was encoded as base64.
We also know that both keys are in the range 0-9999999.

So we run bruteforce first on the outer layer - to decode Blowfish and take all proper base64 results as potential hits.
And then we take those results and try to decode them with DES to look for the flag.
There is slim chance that such long payload decoded with improper Blowfish key would give us base64 string, and in fact we got only a single hit there.
So we run the bruteforecer:

```python
import base64
import string
from Crypto.Cipher import DES, Blowfish
from multiprocessing import freeze_support
from src.crypto_commons.brute.brute import brute


def is_printable(decrypted):
    for i in range(len(decrypted)):
        if decrypted[i] not in string.printable:
            return False
    return True


def combine(partials):
    results = {}
    for partial in partials:
        for key, value in partial.items():
            results[key] = value
    return results


def worker_blowfish(data):
    first, payload = data
    results = {}
    for i in range(10000000):
        key = str(first) + '{:07}'.format(i)
        e = Blowfish.new(key)
        decrypted = e.decrypt(payload)[8:]
        try:
            if is_printable(decrypted[:-8]):
                real_data = base64.b64decode(decrypted)[8:]
                results[key] = real_data
                print('potential match ', key, real_data)
        except:
            pass
    return results


def worker_des(data):
    first, payload = data
    results = {}
    for i in range(10000000):
        key = str(first) + '{:07}'.format(i)
        e = DES.new(key)
        decrypted = e.decrypt(payload)[8:]
        if is_printable(decrypted[:-8]):
            results[key] = decrypted
            print('potential flag ', key, decrypted)
    return results


def main():
    cipher = base64.b64decode(
        'AiEjLYxiRUlgG+OYaYje5HOwvS8UFegdXRrCsIiy6pBH67fDvGbLF/gtZihyW7WYVOrsi7/N1sgaVUBU/VW1NwEOrOhguZZfP5T7Gw88sMx9KFepLfsjOLPKKVUuMbVu6Lno0FJjbU+7ft1VtdsQhAh1Lc91SDcduoI3J1FwffwwEwy1L7FKjg14LZ9fgaMF5c43T8avL+bpOBDFHiPzK1Mwv4ftVt6k5UV13cPV3VLm+Jx7Q/7LLamyQLLUU0O1pcKZOHi7oYPngpFh7VmIPIJwCsmoCAyt8+yC/uqNgpfUoD0SHfG7tvz7F8sZKL6RfezLvFN++8B+rs+6AGOiSHCmnGbO4PNcOdZfWP4lYZQRIZ/DTN4ntg==')
    data = [(i, cipher) for i in range(10)]
    partials = brute(worker_blowfish, data, 10)
    candidates = combine(partials)
    print(candidates)

    for candidate_key, candidate_value in candidates.items():
        data = [(i, candidate_value) for i in range(10)]
        partials = brute(worker_des, data, 10)
        print(combine(partials))


if __name__ == '__main__':
    freeze_support()
    main()
```

where brute() comes from our crypto-commons and is simply:

```python
import multiprocessing


def brute(worker, data_list, processes=8):
    """
    Run multiprocess workers
    :param worker: worker function
    :param data_list: data to distribute between workers, one entry per worker
    :param processes: number of parallel processes
    :return: list of worker return values
    """
    pool = multiprocessing.Pool(processes=processes)
    return pool.map(worker, data_list)
```

From this we get the decoded data:

```
ZeroNights is a perfect place to discuss new attack methods and threats. It shows ways to attack and defend to its guests, and suggests unorthodox approach to cybersecurity problems solving.  
```

###PL version

Generalna idea zadania by??a do???? prosta - autorzy zaszyfrowali flag?? najopiers DESem a potem Blowfishem a naszym zadaniem jest j?? zdekodowa??.

Problemy:

* Autorzy u??yli jakiej?? dziwnej strony do szyfrowania, a nie bezpo??rednio szyfr??w. Ta strona dodawa??a losowy padding i je??li o tym nie wiemy to nie damy rady zrobi?? zadania. Na szcz????cie p????niej zota??o to uj??te jako hint.
* Autorzy bez powodu dodali w zadaniu drugi payload opr??cz flagi. By??o to mocno myl??ce bo suguerowa??o atak meet-in-the-middle, kt??ry by?? tutaj b????dem, poniewa?? przyk??adowy payload u??ywa?? innych kluczy ni?? flaga.
* Obliczenia by??y czasoch??onne ze wzgl??du na rozmiar kluczy. Powa??nie, nie ma potrzeby podawa?? w zadaniu danych wymagajacych minut oblicze?? na 8 r??wnoleg??ych rdzeniach. To wcale nie sprawia ??e zadanie jest "trudniejsze", tylko bardziej wkurzaj??ce.

Mamy dan?? zaszyfrowan?? flag??:

```
AiEjLYxiRUlgG+OYaYje5HOwvS8UFegdXRrCsIiy6pBH67fDvGbLF/gtZihyW7WYVOrsi7/N1sgaVUBU/VW1NwEOrOhguZZfP5T7Gw88sMx9KFepLfsjOLPKKVUuMbVu6Lno0FJjbU+7ft1VtdsQhAh1Lc91SDcduoI3J1FwffwwEwy1L7FKjg14LZ9fgaMF5c43T8avL+bpOBDFHiPzK1Mwv4ftVt6k5UV13cPV3VLm+Jx7Q/7LLamyQLLUU0O1pcKZOHi7oYPngpFh7VmIPIJwCsmoCAyt8+yC/uqNgpfUoD0SHfG7tvz7F8sZKL6RfezLvFN++8B+rs+6AGOiSHCmnGbO4PNcOdZfWP4lYZQRIZ/DTN4ntg==
```

Wiemy ??e flaga zosta??a najpierw zaszyfrowana DESem z paddingiem, nast??pnie enkodowana base64 i zaszyfrowana Blowfishem z paddingiem i zn??w enkodowana base64.
Wiemy ??e klucze s?? z zakresu 0-9999999.

Uruchamiamy wi??c brute-forcer najpierw na zewn??trznej warstwie - aby deszyfrowa?? Blowfisha i wzi???? wszystkie poprawne base64 jako potencjalne trafienia.
Nast??pnie pr??bujemy dekodowa?? je DESem szukaj??c flagi.
Jest niewielka szansa ??e payload dekodowany Blowfishem z losowym kluczem da nam poprawny base64 i faktycznie by?? tylko jeden poprawny ci??g.
Wi??c uruchamiamy bruteforcer:

```python
import base64
import string
from Crypto.Cipher import DES, Blowfish
from multiprocessing import freeze_support
from src.crypto_commons.brute.brute import brute


def is_printable(decrypted):
    for i in range(len(decrypted)):
        if decrypted[i] not in string.printable:
            return False
    return True


def combine(partials):
    results = {}
    for partial in partials:
        for key, value in partial.items():
            results[key] = value
    return results


def worker_blowfish(data):
    first, payload = data
    results = {}
    for i in range(10000000):
        key = str(first) + '{:07}'.format(i)
        e = Blowfish.new(key)
        decrypted = e.decrypt(payload)[8:]
        try:
            if is_printable(decrypted[:-8]):
                real_data = base64.b64decode(decrypted)[8:]
                results[key] = real_data
                print('potential match ', key, real_data)
        except:
            pass
    return results


def worker_des(data):
    first, payload = data
    results = {}
    for i in range(10000000):
        key = str(first) + '{:07}'.format(i)
        e = DES.new(key)
        decrypted = e.decrypt(payload)[8:]
        if is_printable(decrypted[:-8]):
            results[key] = decrypted
            print('potential flag ', key, decrypted)
    return results


def main():
    cipher = base64.b64decode(
        'AiEjLYxiRUlgG+OYaYje5HOwvS8UFegdXRrCsIiy6pBH67fDvGbLF/gtZihyW7WYVOrsi7/N1sgaVUBU/VW1NwEOrOhguZZfP5T7Gw88sMx9KFepLfsjOLPKKVUuMbVu6Lno0FJjbU+7ft1VtdsQhAh1Lc91SDcduoI3J1FwffwwEwy1L7FKjg14LZ9fgaMF5c43T8avL+bpOBDFHiPzK1Mwv4ftVt6k5UV13cPV3VLm+Jx7Q/7LLamyQLLUU0O1pcKZOHi7oYPngpFh7VmIPIJwCsmoCAyt8+yC/uqNgpfUoD0SHfG7tvz7F8sZKL6RfezLvFN++8B+rs+6AGOiSHCmnGbO4PNcOdZfWP4lYZQRIZ/DTN4ntg==')
    data = [(i, cipher) for i in range(10)]
    partials = brute(worker_blowfish, data, 10)
    candidates = combine(partials)
    print(candidates)

    for candidate_key, candidate_value in candidates.items():
        data = [(i, candidate_value) for i in range(10)]
        partials = brute(worker_des, data, 10)
        print(combine(partials))


if __name__ == '__main__':
    freeze_support()
    main()
```

Gdzie brute() jest z naszego crypto-commons i to zwyczajnie:

```python
import multiprocessing


def brute(worker, data_list, processes=8):
    """
    Run multiprocess workers
    :param worker: worker function
    :param data_list: data to distribute between workers, one entry per worker
    :param processes: number of parallel processes
    :return: list of worker return values
    """
    pool = multiprocessing.Pool(processes=processes)
    return pool.map(worker, data_list)
```

Z tego dostajemy zdekodowane dane:

```
ZeroNights is a perfect place to discuss new attack methods and threats. It shows ways to attack and defend to its guests, and suggests unorthodox approach to cybersecurity problems solving.  
```