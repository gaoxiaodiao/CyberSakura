# [pwn 100pts] pwn4 - TAMUctf 19
32ビットバイナリです。
```
$ checksec pwn4
[*] 'pwn4'
    Arch:       32 bits (little endian)
    NX:         NX enabled
    SSP:        SSP disabled (No canary found)
    RELRO:      Partial RELRO
    PIE:        PIE disabled
```
IDAで調べると、`ls %s`にsprintfで入力を入れ、そのコマンドを実行できます。
ただし`/`は使えません。
`;<cmd>`のように入力すれば`ls ;<cmd>`が実行されるので、任意のコマンドを実行できます。

# 感想
簡単なjail系問題です。
