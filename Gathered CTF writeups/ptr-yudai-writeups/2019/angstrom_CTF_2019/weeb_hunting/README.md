# [pwn 230pts] Weeb Hunting - angstromCTF 2019
64bitでSSPは有効です。
```
$ checksec weeb_hunting
[*] 'weeb_hunting'
    Arch:	64 bits (little endian)
    NX:		NX enabled
    SSP:	SSP enabled (Canary found)
    RELRO:	Partial RELRO
    PIE:	PIE disabled
```

RPG風のサービスでアイテムを拾うか戦闘かがランダムで決まります。
戦闘で何でもいいのでアイテムを使えば逃げることができ、アイテムがなければ負けます。
アイテムを拾うと`malloc(0x68)`でweapon構造体が確保され、0〜2のidが設定されます。
アイテムの名前は指定することができます。
戦闘になるとアイテム一覧が表示されるのですが、id<=3のアイテムは表示されません。
また、アイテムを使うとweaponはfreeされますが、グローバル変数からアドレスは消えません。
さらに、アイテムを使うときはidのチェックをしないので、一度取得したアイテムであれば何度も使うことができ、double free脆弱性があります。

ここまでは分かったのですが、競技中は勝手にPIEが有効だと思ってたので（無効でも思いつかなかったかもしれないが）bssセクションにfastbinを向けてグローバル変数を直接いじってやれば良いんですね。
あとは乱数との勝負。

ということで、まずはGOTからlibcのロードアドレスを取得しましょう。
fastbinなのでサイズチェックが入りますが、stdinのアドレスの0x7f...がサイズとして使えるので利用しましょう。
```python
```

# 感想
ROP初心者向けの問題だと思います。
