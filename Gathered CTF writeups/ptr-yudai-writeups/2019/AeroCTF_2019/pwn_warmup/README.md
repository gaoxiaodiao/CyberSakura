# [pwn 100pts] pwn_warmup - Aero CTF 2019
SSPが無効の32ビットバイナリです。
```
$ checksec meme_server
[*] 'meme_server'
    Arch:       32 bits (little endian)
    NX:         NX enabled
    SSP:        SSP disabled (No canary found)
    RELRO:      Partial RELRO
    PIE:        PIE enabled
```
まずパスワードを入力し、`password.txt`の内容と比較します。
入力は次のようになっておりnull-by-offの脆弱性があります。
```
char password[0x20];
int rb = read(0, password, 0x20);
password[rb] = 0;
```
認証用のフラグは始め1にセットされるのですが、null-by-offにより0にできるので認証を突破できます。

# 感想
適当にたくさん入力したら解けるので簡単ですね。