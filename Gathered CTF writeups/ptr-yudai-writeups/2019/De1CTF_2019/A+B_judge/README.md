# [pwn 206pts] A+B Judge - De1CTF 2019
Webサーバーのアドレスが貰えます。
公式writeupにdockerfileも付いていたので起動します。

C言語のプログラムが動かせるジャッジサーバーのようです。
`system("ls -lha")`すると次のようになりました。
```
drwxr-x--- 1 ctf  ctf  4.0K Aug 20 02:19 .
drwxr-xr-x 1 root root 4.0K Aug 20 02:04 ..
-rwxr-x--- 1 root ctf   220 Aug 31  2015 .bash_logout
-rwxr-x--- 1 root ctf  3.7K Aug 31  2015 .bashrc
-rwxr-x--- 1 root ctf   655 Jul 12 19:26 .profile
-rwxr-x--- 1 root ctf    11 Mar 17 23:59 a+b.in
-rwxr-x--- 1 root ctf     6 Mar 17 23:59 a+b.out
-rw-r--r-- 1 ctf  ctf    96 Aug 20 02:19 f967fb18c2f011e99b7c0242ac1d0002.c
-rw-r--r-- 1 ctf  ctf     0 Aug 20 02:19 f967fb18c2f011e99b7c0242ac1d0002.out
-rwxr-xr-x 1 ctf  ctf  8.5K Aug 20 02:19 f967fb18c2f011e99b7c0242ac1d0002_prog
-rwxr----- 1 root ctf    38 Mar 17 23:59 flag
-rwxr-x--x 1 root ctf  3.7K Jul 12 10:43 server.py
-rw-r----- 1 ctf  ctf  3.4K Aug 20 02:06 server.pyc
drwxr-x--- 1 root ctf  4.0K Mar 17 23:59 templates
-rwxr-x--- 1 root ctf    72 Jul 12 10:42 uwsgi.ini
```

また、`system("whoami")`するとRuntime Errorになったりならなかったりしました。
そこで、`system("cat flag")`するとRuntime Errorになったりならなかったりして、ならなかったときにフラグが出力されました。

調べたところ、lorunという個人制作のPythonでサンドボックス実行するライブラリを使っていたらしいのですが、そのライブラリが実際には全然サンドボックスとして機能しないダメダメライブラリだったようです。
想定解はシェルコードを呼び出す方法だったそうです。

# 感想
作問ミスは誰にでもあるのでやむなし。
