# [pwn 50pts] Signed or not signed - INS'hAck 2019
64ビットです。
```
$ checksec -f ./signed_or_not_signed
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   71 Symbols     No	0		2	./signed_or_not_signed
```

IDAで解析するとIntergoverと同じ臭いがします。

数字を入力して大きいと弾かれますが、負の数が入力できるので通ります。

```
$ ./signed_or_not_signed 
Please give me a number:-666
cat: flag.txt: そのようなファイルやディレクトリはありません
```
はい。

# 感想
またもやpwnじゃないやん。