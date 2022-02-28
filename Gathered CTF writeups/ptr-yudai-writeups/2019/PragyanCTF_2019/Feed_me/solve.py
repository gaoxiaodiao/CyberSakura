from ptrlib import *

sock = Socket("127.0.0.1", 9800)

sock.recvline()
r1 = int(sock.recvuntil(" ;").rstrip(b";"))
r2 = int(sock.recvuntil(" ;").rstrip(b";"))
r3 = int(sock.recvuntil(" ;").rstrip(b";"))
dump("(r1, r2, r3) = ({}, {}, {})".format(r1, r2, r3))

x = (r1 + r2 - r3) // 2
y = r2 - x
val = r1 - x

payload1 = str(val)
payload1 += "-" * (10 - len(payload1))
payload2 = str(x)
payload2 += "-" * (10 - len(payload2))
payload3 = str(y)
payload = payload1 + payload2 + payload3

_ = input()
sock.sendline(payload)

sock.interactive()
