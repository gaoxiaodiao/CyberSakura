# [pwn  268pts] offensive honeypot - DefCamp CTF Qualification 2019
64ビットバイナリで、PIEとRELROが無効です。
```
$ checksec -f pwn_honeypot
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols      Yes     0               3       pwn_honeypot
```
IDAで読みます。まずnameに9文字まで入力できます。
なんかplayerとhackerのHPがあって、playerのHPが正の状態でhackerのHPを負にできたらフラグが貰えるようです。
各ラウンドにオプションが選べて、Show menu, Firewall, Battleがあります。
Firewallではdefenceに好きなint整数を代入できます。
defenceはBattleのときに関係あって、defenceの値によってBattleで作られるスレッド内での処理が変わります。defenceが1のとき、`hacker_hp`から`rand() % 0x1e`引いて`usleep(10)`します。2のとき、`hacker_hp`から4引いて`usleep(10)`します。0のとき、`hacker_hp`から3引いて`usleep(0)`します。いずれも終了後にdefenceの値を-1にします。
Battleでは上の処理を動かしている間、defenceに好きなint整数を代入できて、`rand() & 0b11`がdefenceと等しいか調べます。等しければ攻撃を防げます。等しくなければ先程の`rand() & 0b11`の値に応じて`player_hp`からいくらか引かれます。roundは最大200回までです。さて、最初に`srand(time(NULL))`されているので、ランダムが予測できます。ということで、上手いこと攻撃をかわしていい感じに攻撃すれば倒せるのかなーと思います。

```python
from ptrlib import *
import ctypes
import time

glibc = ctypes.cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc-2.27.so')
glibc.srand(glibc.time(0))

randList = []
randCnt = 0
def rand(i):
    if i >= len(randList):
        for j in range(i - len(randList) + 1):
            randList.append(glibc.rand())
    return randList[i]

def firewall(option):
    sock.sendlineafter("Enter option:", "2")
    sock.sendlineafter("Option: ", str(option))
    return

def activate(option):
    sock.sendlineafter("Enter option:", "3")
    time.sleep(0.01)
    sock.sendlineafter("Option: ", str(option))

def get_state():
    sock.recvuntil("round : ")
    r = int(sock.recvline())
    sock.recvuntil(": ")
    player_hp = int(sock.recvline())
    sock.recvuntil(": ")
    hacker_hp = int(sock.recvline())
    sock.recvuntil(": ")
    defence = int(sock.recvline())
    return r, player_hp, hacker_hp, defence

#sock = Process("./pwn_honeypot")
sock = Socket("localhost", 9000)
sock.sendlineafter("\n", "taro")

while True:
    r, myhp, hp, defence = get_state()
    if hp < 0: break

    if rand(randCnt) % 0x1e > 4:
        firewall(1)
        randCnt += 1
    else:
        firewall(2)
    activate(rand(randCnt) & 0b11)
    randCnt += 1

sock.interactive()
```

ほい。
```
$ python solve.py 
[+] __init__: Successfully connected to localhost:9000
[ptrlib]$ You won: 
FLAG{dummy_flag}
```

# 感想
pwnというかmiscですね。