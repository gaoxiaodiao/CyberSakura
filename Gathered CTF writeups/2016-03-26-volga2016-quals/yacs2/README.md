## YACS2 - yet another captcha solver (PPC)

###ENG
[PL](#pl-version)

The task looks very similar to the one from last year - we have a captcha recorded in a .wav file.
The captcha contains only numbers.
We are supposed to solve 3000 of them to get the flag.
Apart from that the captcha is distorted by a constant background noise.

Example: [captcha](captcha.wav)

We solved this with very little effort, using solver we developed last year.
The fun part is that this solver was not good enough last year and we had to make a different one, but this time it worked out-of-the-box.

Instead of trying to remove the noise and then match some byte patterns for numbers, we just used Google Speech Recognition :)

So we just download the captcha, solve it, send response and repeat this 3000 times to get the flag.

```python
import codecs
import os
import urllib
import urllib2
import speech_recognition as sr

url = 'http://yacst2.2016.volgactf.ru:8090/captcha'

opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', 'JSESSIONID=s4Re0bJa4po1O8wPS9yGxF9FKxO4afQEnJbhhjiZ'))

post_opener = urllib2.build_opener(urllib2.HTTPHandler())
post_opener.addheaders.append(('Cookie', 'JSESSIONID=s4Re0bJa4po1O8wPS9yGxF9FKxO4afQEnJbhhjiZ'))


def download_wav():
    wav = opener.open(url).read()
    with codecs.open("captcha.wav", mode="wb") as output:
        output.write(wav)


def convert_to_speech2():
    r = sr.Recognizer()
    with sr.WavFile('captcha.wav') as source:
        audio = r.record(source)
        return r.recognize(audio)

def send_response(result):
    try:
        data = urllib.urlencode({'captcha': result})
        return post_opener.open(url, data=data).read()
    except:
        pass


def removeFile():
    os.remove("captcha.wav")


def main():
    for i in range(3000):
        try:
            print(i)
            download_wav()
            result = convert_to_speech2()
            print(result)
            removeFile()
            response = send_response(result)
        except:
            pass

main()
```

After the last one we are redirected to the flag:

`VolgaCTF{Sound IS L1ke M@th if A+B=C THEN C-B=A}`

###PL version

Zadanie jest bardzo podobne do zadania z zesz??ego roku - mamy d??wi??kowy kod captcha zapisany w pliku .wav.
Captcha zawiera tylko liczby.
Mamy do rozwi??zania 3000 kod??w aby uzyska?? flag??.
Dodatkowo captcha jest zniekszta??cona poprzez dodanie sta??ego d??wi??ku w tle.

Przyk??ad: [captcha](captcha.wav)

Rozwi??zali??my to zadanie bardzo niewielkim nak??adem pracy, u??ywaj??c solvera napisanego rok temu.
Co ciekawe, rok temu ten solver nie by?? wystarczaj??co dobry i musieli??my zrobi?? inny, ale tym razem zadzia??a?? od razu.

Zamiast pr??bowa?? usuwa?? zniekszta??cenie a nast??pnie dopasowywa?? wzorce bajt??w do numer??w w captchy, u??yli??my Google Speech Recognition :)

Pobieramy wi??c captche, rozwi??zujemy j?? i odsy??amy wynik, to wszystko powtarzamy 3000 razy i dostajemy flag??.

```python
import codecs
import os
import urllib
import urllib2
import speech_recognition as sr

url = 'http://yacst2.2016.volgactf.ru:8090/captcha'

opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', 'JSESSIONID=s4Re0bJa4po1O8wPS9yGxF9FKxO4afQEnJbhhjiZ'))

post_opener = urllib2.build_opener(urllib2.HTTPHandler())
post_opener.addheaders.append(('Cookie', 'JSESSIONID=s4Re0bJa4po1O8wPS9yGxF9FKxO4afQEnJbhhjiZ'))


def download_wav():
    wav = opener.open(url).read()
    with codecs.open("captcha.wav", mode="wb") as output:
        output.write(wav)


def convert_to_speech2():
    r = sr.Recognizer()
    with sr.WavFile('captcha.wav') as source:
        audio = r.record(source)
        return r.recognize(audio)

def send_response(result):
    try:
        data = urllib.urlencode({'captcha': result})
        return post_opener.open(url, data=data).read()
    except:
        pass


def removeFile():
    os.remove("captcha.wav")


def main():
    for i in range(3000):
        try:
            print(i)
            download_wav()
            result = convert_to_speech2()
            print(result)
            removeFile()
            response = send_response(result)
        except:
            pass

main()
```

Po ostatnim kodzie zostajemy przekierowani do flagi:

`VolgaCTF{Sound IS L1ke M@th if A+B=C THEN C-B=A}`
