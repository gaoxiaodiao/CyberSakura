from ptrlib import *
import base64

sock = Socket("ugm.cybrics.net", 110)

sock.recvline()
sock.sendline("USER fawkes")
sock.recvline()
sock.sendline("PASS Combin4t1onXXY")
sock.recvline()
sock.sendline("RETR 1")
sock.recvuntil("base64\r\n\r\n")
data = b''
while True:
    data += sock.recv()
    if b'\r\n\r\n' in data:
        data = data[:data.index(b'\r\n\r\n')]
        break

binary = base64.b64decode(data)
with open("secret_flag.zip", "wb") as f:
    f.write(binary)
