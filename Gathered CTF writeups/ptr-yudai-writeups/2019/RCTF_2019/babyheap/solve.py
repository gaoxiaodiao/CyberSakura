from ptrlib import *

def add(size):
    sock.recvuntil("Choice: \n")
    sock.sendline("1")
    sock.recvuntil("Size: ")
    sock.sendline(str(size))

def edit(index, data):
    sock.recvuntil("Choice: \n")
    sock.sendline("2")
    sock.recvuntil("Index: ")
    sock.sendline(str(index))
    sock.recvuntil("Content: ")
    sock.send(data)

def delete(index):
    sock.recvuntil("Choice: \n")
    sock.sendline("3")
    sock.recvuntil("Index: ")
    sock.sendline(str(index))

def show(index):
    sock.recvuntil("Choice: \n")
    sock.sendline("4")
    sock.recvuntil("Index: ")
    sock.sendline(str(index))

libc = ELF("./libc-2.23.so")
sock = Socket("localhost", 9999)

# null byte poisoning

sock.interactive()
