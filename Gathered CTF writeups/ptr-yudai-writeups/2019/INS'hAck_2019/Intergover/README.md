# [pwn 50pts] Intergover - INS'hAck 2019
64ビットでSSPが有効です。
```
$ checksec -f intergover
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   73 Symbols     Yes	0		2	intergover
```

IDAで解析すると、数字を入力して結果が0xf2ならOKっぽいです。
```
$ ./intergover 
Give me one param: 242
cat: flag.txt: そのようなファイルやディレクトリはありません
```

は？これだけ？

# 感想
pwnじゃないやん。