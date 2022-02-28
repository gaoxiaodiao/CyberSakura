# [pwn 500pts] rellocator - Backdoor CTF 2019
64ビットバイナリで、全部有効です。
```
$ checksec -f rellocator
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes     0               2       rellocator
```
最初に謎に自由なサイズのmallocができます。メインループではMalloc, Relloc, Viewができます。
Mallocでは0から0x58までのmallocができます。Viewでは最初のサイズ分だけしっかりwriteで出力します。Rellocではreallocで0から0x58までのサイズに変更できます。freeがありませんが、reallocでfreeの変わりになるでしょう。Rellocの後に呼ばれるreadline的なものにはoff-by-nullがあります。

サイズ0x58までだしoff-by-nullでは無理では？

# 感想
誰も解けてないっぽいので放置。
