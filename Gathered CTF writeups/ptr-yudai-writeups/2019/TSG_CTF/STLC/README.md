# [pwn 500pts] STLC - TSG CTF
64ビットでもちろん全部有効です。
```
$ checksec -f stlc
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   824 Symbols     Yes     0               4       stlc
```
なんかラムダ式が定義、計算できるバイナリっぽい。ラムダ式嫌い。
まぁ競技中に誰も解けなかった問題を私が解けるはずもないので公式writeup(参考文献[1])を読みます。
（というかこんなクソデカC++バイナリを競技中に解析できる妖怪はいないと信じたい......）

とりあえず普通に使ってみます。
問題文に使用例があるのでなんとなく使い方が分かるかなーと思ったのですが大学で習ったのと記法が全然違ってハゲました。
[ここ](http://proofcafe.org/sf/Stlc_J.html)を参考にもしましたが、若干違うようです。（複数の引数は定義できない？）
```
> f = (\x:A. x)
f = (\x:A.x) :: (A->A)
```

decは最初から定義されています。

# 感想
難しいという事実以外分からない。

# 参考文献
[1] https://gist.github.com/satos---jp/e778ac2f3c58cf3f56e8f2e37fd69b84