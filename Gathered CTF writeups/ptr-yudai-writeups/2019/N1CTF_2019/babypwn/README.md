# [pwn 400pts] BabyPwn - N1CTF 2019
64ビットバイナリで、PIE以外有効です。
```
$ checksec -f BabyPwn
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      Yes     0               2       BabyPwn
```
addとdeleteがあるヒープ系です。
addでは10個の中から空いている場所が選ばれ、`buf = malloc(0x20)`されます。
で、bufの先頭0x10バイトはnameになり、0x10バイト目にはdescriptionのアドレス、0x18バイト目にはサイズが入ります。サイズは0から0xffの中から選べます。
deleteでは`free(buf[i]);`して終わります。
ということで、単純なdouble freeがあります。
しかしまたshow系が無いのでstdoutで頑張ります。（正直これ面倒なだけだからbaby問ではやめてほしい。）

面倒なので（ちゃんとlibcリークはしますが）ASLRは無効にしてやりました。
libcは配られていないのですが、2.23らしいです。（たぶん接続して適当にdouble freeしたときのエラーで分かるんだと思います。）

double freeできるのはサイズ0x30のチャンクだけです。とりあえず偽のチャンクを作ってそこにchunk overlapしてやる方向で考えましょう。



# 感想
面倒ですね。
