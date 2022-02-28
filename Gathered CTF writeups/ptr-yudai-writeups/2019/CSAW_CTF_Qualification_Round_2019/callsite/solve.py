from ptrlib import *

sock = Socket("rev.chal.csaw.io", 1001)
sock.recvline()
sock.sendline("400cbb whatever")

sock.interactive()
