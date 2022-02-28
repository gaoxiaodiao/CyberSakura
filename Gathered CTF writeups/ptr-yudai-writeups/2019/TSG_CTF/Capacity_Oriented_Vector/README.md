# [pwn 499pts] Capacirt Oriented Vector - TSG CTF
64ビットで全部有効です。
```
$ checksec -f vector
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   93 Symbols     Yes	0		4	vector
```
さすがにバイナリが大きすぎて読む気にならないのでソースコードを読みます。

最大100個までベクターを作ることができ、ベクターにはサイズと容量が記憶されています。
ベクターを作るときに容量を設定し、そのサイズだけ確保されます。
pushするとサイズが増え、setで変更できます。
set_atでグローバル変数vectorsに、生成したベクタが登録されます。



# 感想

# 参考文献
