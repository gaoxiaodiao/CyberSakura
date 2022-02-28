# [pwn 305pts] Baby0x02 - SEC-T CTF 2019
64ビットバイナリで、全部有効です。
```
$ checksec -f chall
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes     0               3       chall
```
IDAで解析すると指定したファイルを読んでくれるプログラムであることが分かります。
SEC-Tの他のpwnのフラグが`flag`という名前だったことから、ファイル名にflagを指定すれば読み込めました。

# 感想
......？