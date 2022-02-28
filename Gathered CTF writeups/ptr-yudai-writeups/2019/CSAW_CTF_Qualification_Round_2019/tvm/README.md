# [pwn 400pts] tvm - CSAW CTF Qualification 2019
64ビットバイナリで、PIE以外有効です。
```
$ checksec -f tvm
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      Yes     0               3       tvm
```
結論から言うと、ただのrev問でpwn要素はほとんどありませんでした。
vmの仕様書が渡されるのですが、そこに書かれていないヒープのアドレスをリークする命令があるので、それを使えば鍵とIVのアドレスを計算でき、リークした鍵とIVで暗号化されたフラグを復号できます。

# 感想
rev要素で難しくするvm問嫌い。
